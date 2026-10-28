<?php
/**
 * CMS Handoff Executor v1.0
 *
 * Lives in wp-content/novamira-sandbox/cms-executor.php. Defines functions only:
 * nothing runs on load. Called through Novamira execute-php:
 *
 *   return cms_exec( 'preflight', 'client-slug' );
 *   return cms_exec( 'stage',     'client-slug', array( 'run_id' => '20261028-1400' ) );
 *   return cms_exec( 'apply',     'client-slug', array( 'run_id' => '...', 'phase' => 'pages', 'offset' => 0 ) );
 *   return cms_exec( 'apply',     'client-slug', array( 'run_id' => '...', 'phase' => 'site' ) );
 *   return cms_exec( 'verify',    'client-slug' );
 *   return cms_exec( 'rollback',  'client-slug', array( 'run_id' => '...' ) );
 *
 * Reads wp-content/uploads/cms-handoff/<client>/bundle.json (built by build_bundle.py).
 * Writes a JSONL change log to .../cms-handoff/<client>/logs/<run_id>.jsonl.
 * Returns compact summaries only, so the model's context stays small.
 */

if ( ! defined( 'ABSPATH' ) ) {
	return;
}

if ( ! function_exists( 'cms_exec' ) ) {

	define( 'CMS_EXEC_VERSION', '1.0' );
	define( 'CMS_EXEC_TIME_BUDGET', 22.0 ); // Novamira execute-php limit is 30s.

	/* ------------------------------------------------------------------ */
	/* Entry point                                                         */
	/* ------------------------------------------------------------------ */

	function cms_exec( $command, $client, $opts = array() ) {
		$start  = microtime( true );
		$bundle = cms_exec_load( $client );
		if ( is_wp_error( $bundle ) ) {
			return array( 'ok' => false, 'error' => $bundle->get_error_message() );
		}
		$ctx = array(
			'client' => sanitize_key( $client ),
			'bundle' => $bundle,
			'run_id' => isset( $opts['run_id'] ) ? preg_replace( '/[^0-9A-Za-z\-_]/', '', $opts['run_id'] ) : gmdate( 'Ymd-His' ),
			'start'  => $start,
			'sum'    => array( 'changed' => 0, 'unchanged' => 0, 'created' => 0, 'skipped' => 0, 'errors' => 0, 'warnings' => 0 ),
			'issues' => array(),
		);

		switch ( $command ) {
			case 'preflight':
				cms_exec_preflight( $ctx );
				break;
			case 'stage':
				if ( ! cms_exec_gate( $ctx, false ) ) {
					break;
				}
				cms_exec_stage( $ctx, $opts );
				break;
			case 'apply':
				if ( ! cms_exec_gate( $ctx, true ) ) {
					break;
				}
				$phase = isset( $opts['phase'] ) ? $opts['phase'] : 'pages';
				if ( 'site' === $phase ) {
					cms_exec_apply_site( $ctx );
				} else {
					cms_exec_apply_pages( $ctx, $opts );
				}
				break;
			case 'verify':
				cms_exec_verify( $ctx );
				break;
			case 'rollback':
				if ( empty( $opts['run_id'] ) ) {
					return array( 'ok' => false, 'error' => 'rollback needs run_id' );
				}
				cms_exec_rollback( $ctx );
				break;
			default:
				return array( 'ok' => false, 'error' => 'unknown command: ' . $command );
		}

		$out = array(
			'ok'       => 0 === $ctx['sum']['errors'],
			'command'  => $command,
			'client'   => $ctx['client'],
			'run_id'   => $ctx['run_id'],
			'version'  => CMS_EXEC_VERSION,
			'counts'   => $ctx['sum'],
			'issues'   => array_slice( $ctx['issues'], 0, 60 ),
			'seconds'  => round( microtime( true ) - $start, 1 ),
		);
		if ( count( $ctx['issues'] ) > 60 ) {
			$out['issues_truncated'] = count( $ctx['issues'] ) - 60;
		}
		if ( isset( $ctx['next_offset'] ) ) {
			$out['next_offset'] = $ctx['next_offset'];
		}
		if ( isset( $ctx['next_step'] ) ) {
			$out['next_step'] = $ctx['next_step'];
		}
		return $out;
	}

	/* ------------------------------------------------------------------ */
	/* Loading, gates, logging                                             */
	/* ------------------------------------------------------------------ */

	function cms_exec_dir( $client ) {
		$u = wp_upload_dir();
		return trailingslashit( $u['basedir'] ) . 'cms-handoff/' . sanitize_key( $client );
	}

	function cms_exec_protect_dir( $dir ) {
		if ( ! is_dir( $dir ) ) {
			wp_mkdir_p( $dir );
		}
		if ( ! file_exists( $dir . '/.htaccess' ) ) {
			file_put_contents( $dir . '/.htaccess', "Require all denied\nDeny from all\n" );
		}
		if ( ! file_exists( $dir . '/index.html' ) ) {
			file_put_contents( $dir . '/index.html', '' );
		}
	}

	function cms_exec_load( $client ) {
		$dir = cms_exec_dir( $client );
		cms_exec_protect_dir( dirname( $dir ) );
		cms_exec_protect_dir( $dir );
		$f = $dir . '/bundle.json';
		if ( ! file_exists( $f ) ) {
			return new WP_Error( 'no_bundle', 'bundle.json not found at ' . $f );
		}
		$b = json_decode( file_get_contents( $f ), true );
		if ( ! is_array( $b ) ) {
			return new WP_Error( 'bad_bundle', 'bundle.json is not valid JSON' );
		}
		if ( ! isset( $b['schema_version'] ) || '1.0' !== $b['schema_version'] ) {
			return new WP_Error( 'bad_version', 'bundle schema_version must be 1.0' );
		}
		if ( empty( $b['built_by'] ) || 'build_bundle.py' !== $b['built_by'] ) {
			return new WP_Error( 'not_built', 'bundle.json must be produced by build_bundle.py (validation step)' );
		}
		return $b;
	}

	/** NOV-04 backup gate, approval gate, and (for apply) review gate. */
	function cms_exec_gate( &$ctx, $is_apply ) {
		$b  = $ctx['bundle'];
		$ok = true;
		if ( empty( $b['approved']['by'] ) ) {
			cms_exec_issue( $ctx, 'error', '-', 'approved.by is empty: the handoff is not approved' );
			$ok = false;
		}
		$ts = isset( $b['backup']['timestamp'] ) ? strtotime( $b['backup']['timestamp'] ) : false;
		if ( empty( $b['backup']['confirmed'] ) || ! $ts || ( time() - $ts ) > DAY_IN_SECONDS ) {
			cms_exec_issue( $ctx, 'error', '-', 'backup not confirmed within the last 24 hours (NOV-04)' );
			$ok = false;
		}
		if ( $is_apply && empty( $b['review']['confirmed'] ) ) {
			cms_exec_issue( $ctx, 'error', '-', 'review.confirmed is false: a human must review staged drafts before apply (NOV-07)' );
			$ok = false;
		}
		return $ok;
	}

	function cms_exec_log( &$ctx, $entry ) {
		$dir = cms_exec_dir( $ctx['client'] ) . '/logs';
		cms_exec_protect_dir( $dir );
		$entry['ts']  = gmdate( 'c' );
		$entry['run'] = $ctx['run_id'];
		file_put_contents( $dir . '/' . $ctx['run_id'] . '.jsonl', wp_json_encode( $entry ) . "\n", FILE_APPEND | LOCK_EX );
	}

	function cms_exec_issue( &$ctx, $level, $page, $msg ) {
		if ( 'error' === $level ) {
			$ctx['sum']['errors']++;
		} elseif ( 'warning' === $level ) {
			$ctx['sum']['warnings']++;
		}
		$ctx['issues'][] = array( 'level' => $level, 'page' => $page, 'msg' => $msg );
	}

	function cms_exec_out_of_time( $ctx ) {
		return ( microtime( true ) - $ctx['start'] ) > CMS_EXEC_TIME_BUDGET;
	}

	/* ------------------------------------------------------------------ */
	/* Resolving pages                                                     */
	/* ------------------------------------------------------------------ */

	function cms_exec_path( $url ) {
		$p = wp_parse_url( $url, PHP_URL_PATH );
		return trim( (string) $p, '/' );
	}

	/** Find a post by path, any status except trash. */
	function cms_exec_find( $url, $post_type = 'page' ) {
		$path = cms_exec_path( $url );
		if ( '' === $path ) {
			$front = (int) get_option( 'page_on_front' );
			return $front ? get_post( $front ) : null;
		}
		$types = array_unique( array( $post_type, 'page', 'post' ) );
		$p     = get_page_by_path( $path, OBJECT, $types );
		if ( $p && 'trash' !== $p->post_status ) {
			return $p;
		}
		$id = url_to_postid( home_url( '/' . $path . '/' ) );
		return $id ? get_post( $id ) : null;
	}

	function cms_exec_target( &$ctx, $pg ) {
		if ( ! empty( $pg['post_id'] ) ) {
			$p = get_post( (int) $pg['post_id'] );
			if ( ! $p ) {
				cms_exec_issue( $ctx, 'error', $pg['id'], 'post_id ' . $pg['post_id'] . ' not found' );
				return null;
			}
			if ( cms_exec_path( get_permalink( $p ) ) !== cms_exec_path( $pg['url'] ) && 'publish' === $p->post_status ) {
				cms_exec_issue( $ctx, 'warning', $pg['id'], 'post_id path differs from handoff url (' . cms_exec_path( get_permalink( $p ) ) . ')' );
			}
			return $p;
		}
		return cms_exec_find( $pg['url'], isset( $pg['post_type'] ) ? $pg['post_type'] : 'page' );
	}

	/** Staged draft for a create page (identified by handoff meta). */
	function cms_exec_staged( $ctx, $pg, $meta_key ) {
		$q = get_posts(
			array(
				'post_type'      => 'any',
				'post_status'    => array( 'draft', 'pending', 'private', 'publish' ),
				'meta_key'       => $meta_key,
				'meta_value'     => $ctx['client'] . ':' . $pg['id'],
				'posts_per_page' => 1,
				'fields'         => 'ids',
			)
		);
		return $q ? get_post( $q[0] ) : null;
	}

	/* ------------------------------------------------------------------ */
	/* Field writers (idempotent, logged)                                  */
	/* ------------------------------------------------------------------ */

	function cms_exec_set_meta( &$ctx, $pid, $page, $key, $val ) {
		$old = (string) get_post_meta( $pid, $key, true );
		$val = (string) $val;
		if ( $old === $val ) {
			$ctx['sum']['unchanged']++;
			return;
		}
		if ( '' === $val ) {
			delete_post_meta( $pid, $key );
		} else {
			update_post_meta( $pid, $key, $val );
		}
		cms_exec_log( $ctx, array( 'type' => 'meta', 'page' => $page, 'post' => $pid, 'key' => $key, 'old' => $old, 'new' => $val ) );
		$ctx['sum']['changed']++;
	}

	function cms_exec_set_field( &$ctx, $pid, $page, $field, $val ) {
		$old = (string) get_post_field( $field, $pid );
		if ( $old === (string) $val ) {
			$ctx['sum']['unchanged']++;
			return true;
		}
		$r = wp_update_post( wp_slash( array( 'ID' => $pid, $field => $val ) ), true );
		if ( is_wp_error( $r ) ) {
			cms_exec_issue( $ctx, 'error', $page, $field . ': ' . $r->get_error_message() );
			return false;
		}
		cms_exec_log( $ctx, array( 'type' => 'field', 'page' => $page, 'post' => $pid, 'key' => $field, 'old' => $old, 'new' => (string) $val ) );
		$ctx['sum']['changed']++;
		return true;
	}

	function cms_exec_set_content( &$ctx, $pid, $page, $content ) {
		$old = (string) get_post_field( 'post_content', $pid );
		if ( $old === $content ) {
			$ctx['sum']['unchanged']++;
			return true;
		}
		$rev = wp_save_post_revision( $pid );
		$r   = wp_update_post( wp_slash( array( 'ID' => $pid, 'post_content' => $content ) ), true );
		if ( is_wp_error( $r ) ) {
			cms_exec_issue( $ctx, 'error', $page, 'content: ' . $r->get_error_message() );
			return false;
		}
		cms_exec_log( $ctx, array( 'type' => 'content', 'page' => $page, 'post' => $pid, 'revision' => $rev ? (int) $rev : 0, 'old_len' => strlen( $old ), 'new_len' => strlen( $content ) ) );
		$ctx['sum']['changed']++;
		return true;
	}

	/** SEOPress title + description (META-01, NOV-02). */
	function cms_exec_seo( &$ctx, $pid, $pg ) {
		if ( isset( $pg['seo_title'] ) ) {
			cms_exec_set_meta( $ctx, $pid, $pg['id'], '_seopress_titles_title', $pg['seo_title'] );
		}
		if ( isset( $pg['meta_description'] ) ) {
			cms_exec_set_meta( $ctx, $pid, $pg['id'], '_seopress_titles_desc', preg_replace( '/\s+/', ' ', $pg['meta_description'] ) );
		}
	}

	/** Where does this page's visible H1 come from? */
	function cms_exec_h1_mode( $post ) {
		$n = preg_match_all( '#<h1\b[^>]*>.*?</h1>#is', (string) $post->post_content );
		if ( 1 === $n ) {
			return 'content';
		}
		if ( $n > 1 ) {
			return 'multiple';
		}
		$hide = get_post_meta( $post->ID, '_kad_post_title', true );
		return ( 'hide' === $hide ) ? 'hidden' : 'title';
	}

	function cms_exec_h1_block( $text ) {
		return "<!-- wp:heading {\"level\":1} -->\n<h1 class=\"wp-block-heading\">" . esc_html( $text ) . "</h1>\n<!-- /wp:heading -->\n\n";
	}

	function cms_exec_set_h1( &$ctx, $post, $pg ) {
		if ( empty( $pg['h1'] ) ) {
			return;
		}
		$post = get_post( $post->ID );
		$mode = cms_exec_h1_mode( $post );
		if ( 'content' === $mode ) {
			$h1      = esc_html( $pg['h1'] );
			$content = preg_replace_callback(
				'#(<h1\b[^>]*>)(.*?)(</h1>)#is',
				function ( $m ) use ( $h1 ) {
					return $m[1] . $h1 . $m[3];
				},
				$post->post_content,
				1
			);
			cms_exec_set_content( $ctx, $post->ID, $pg['id'], $content );
		} elseif ( 'title' === $mode ) {
			cms_exec_set_field( $ctx, $post->ID, $pg['id'], 'post_title', $pg['h1'] );
		} elseif ( 'hidden' === $mode ) {
			cms_exec_set_content( $ctx, $post->ID, $pg['id'], cms_exec_h1_block( $pg['h1'] ) . $post->post_content );
			cms_exec_issue( $ctx, 'warning', $pg['id'], 'theme title hidden: H1 inserted as first content block' );
		} else {
			cms_exec_issue( $ctx, 'error', $pg['id'], 'page has more than one H1: H1 not written, fix by hand (H1-01)' );
		}
	}

	/* ------------------------------------------------------------------ */
	/* PREFLIGHT (read-only)                                               */
	/* ------------------------------------------------------------------ */

	function cms_exec_preflight( &$ctx ) {
		$b = $ctx['bundle'];
		cms_exec_gate( $ctx, false );
		$engine = cms_exec_redirect_engine();
		if ( ! $engine && ! empty( $b['redirects'] ) ) {
			cms_exec_issue( $ctx, 'error', '-', 'no redirect engine (Redirection or SEOPress Pro) active' );
		}
		$ctx['issues'][] = array( 'level' => 'info', 'page' => '-', 'msg' => 'redirect engine: ' . ( $engine ? $engine : 'none' ) . '; pages: ' . count( $b['pages'] ) . '; redirects: ' . count( $b['redirects'] ) );

		foreach ( $b['pages'] as $pg ) {
			$t = cms_exec_target( $ctx, $pg );
			if ( 'create' === $pg['action'] ) {
				$staged = cms_exec_staged( $ctx, $pg, '_cms_handoff' );
				if ( $t && ( ! $staged || $staged->ID !== $t->ID ) ) {
					cms_exec_issue( $ctx, 'error', $pg['id'], 'create: URL already taken by post ' . $t->ID . ' (' . $t->post_status . '); would produce a -2 slug (URL-04)' );
				}
				$parent_path = trim( dirname( '/' . cms_exec_path( $pg['url'] ) ), '/.' );
				if ( '' !== $parent_path && ! cms_exec_find( '/' . $parent_path . '/' ) ) {
					cms_exec_issue( $ctx, 'error', $pg['id'], 'parent page /' . $parent_path . '/ does not exist' );
				}
				$ctx['sum']['skipped']++;
				continue;
			}
			if ( ! $t ) {
				cms_exec_issue( $ctx, 'error', $pg['id'], 'update: no page found at ' . $pg['url'] );
				continue;
			}
			$mode = cms_exec_h1_mode( $t );
			if ( 'multiple' === $mode ) {
				cms_exec_issue( $ctx, 'error', $pg['id'], 'more than one H1 on page (post ' . $t->ID . ')' );
			} elseif ( 'hidden' === $mode ) {
				cms_exec_issue( $ctx, 'warning', $pg['id'], 'theme title hidden and no H1 in content: H1 will be inserted as first block' );
			}
			if ( 'publish' !== $t->post_status && empty( $pg['publish'] ) ) {
				cms_exec_issue( $ctx, 'warning', $pg['id'], 'target is ' . $t->post_status . ' and the handoff does not publish it' );
			}
			if ( ! empty( $pg['publish'] ) && 'publish' !== $t->post_status && $t->post_name !== basename( cms_exec_path( $pg['url'] ) ) ) {
				cms_exec_issue( $ctx, 'error', $pg['id'], 'draft slug "' . $t->post_name . '" does not match handoff url' );
			}
			$taken = cms_exec_find( $pg['url'] );
			if ( ! empty( $pg['publish'] ) && $taken && $taken->ID !== $t->ID && 'publish' === $taken->post_status ) {
				cms_exec_issue( $ctx, 'error', $pg['id'], 'url already used by published post ' . $taken->ID );
			}
			$ctx['sum']['unchanged']++;
		}

		foreach ( $b['redirects'] as $r ) {
			$existing = cms_exec_redirect_lookup( $engine, $r['from'] );
			if ( $existing && untrailingslashit( $existing['to'] ) !== untrailingslashit( cms_exec_rel( $r['to'] ) ) ) {
				cms_exec_issue( $ctx, 'error', $r['from'], 'existing redirect points to ' . $existing['to'] . ' (handoff says ' . $r['to'] . ')' );
			}
			$dest = cms_exec_find( $r['to'] );
			if ( ! $dest && '' !== cms_exec_path( $r['to'] ) ) {
				$in_handoff = false;
				foreach ( $b['pages'] as $pg ) {
					if ( cms_exec_path( $pg['url'] ) === cms_exec_path( $r['to'] ) ) {
						$in_handoff = true;
					}
				}
				if ( ! $in_handoff ) {
					cms_exec_issue( $ctx, 'error', $r['from'], 'redirect target ' . $r['to'] . ' does not exist and is not created by this handoff' );
				}
			}
		}
		foreach ( $b['noindex'] as $n ) {
			if ( ! cms_exec_find( $n['url'] ) ) {
				cms_exec_issue( $ctx, 'error', $n['url'], 'noindex: page not found' );
			}
		}
	}

	/* ------------------------------------------------------------------ */
	/* STAGE: create drafts for new pages + preview drafts for rebuilds    */
	/* Nothing live changes in this step.                                  */
	/* ------------------------------------------------------------------ */

	function cms_exec_stage( &$ctx, $opts ) {
		$b = $ctx['bundle'];
		foreach ( $b['pages'] as $pg ) {
			if ( cms_exec_out_of_time( $ctx ) ) {
				$ctx['next_step'] = 'out of time: run stage again with the same run_id (already-staged pages are skipped)';
				return;
			}
			if ( 'create' === $pg['action'] ) {
				cms_exec_stage_create( $ctx, $pg );
			} elseif ( 'build' === $pg['route'] && 'update' === $pg['action'] ) {
				cms_exec_stage_preview( $ctx, $pg );
			} else {
				$ctx['sum']['skipped']++;
			}
		}
		$ctx['next_step'] = 'Human VA reviews/styles every draft listed in the handoff review file, adds images, then sets review.confirmed = true and re-uploads the bundle before apply.';
	}

	function cms_exec_stage_create( &$ctx, $pg ) {
		$existing = cms_exec_staged( $ctx, $pg, '_cms_handoff' );
		if ( $existing ) {
			$ctx['sum']['unchanged']++;
			return;
		}
		if ( cms_exec_find( $pg['url'], $pg['post_type'] ) ) {
			cms_exec_issue( $ctx, 'error', $pg['id'], 'URL already taken: refusing to create a -N slug (URL-04)' );
			return;
		}
		$path   = cms_exec_path( $pg['url'] );
		$slug   = basename( $path );
		$parent = 0;
		$pp     = trim( dirname( '/' . $path ), '/.' );
		if ( '' !== $pp ) {
			$par = cms_exec_find( '/' . $pp . '/' );
			if ( ! $par ) {
				cms_exec_issue( $ctx, 'error', $pg['id'], 'parent /' . $pp . '/ missing' );
				return;
			}
			$parent = $par->ID;
		}
		$id = wp_insert_post(
			wp_slash(
				array(
					'post_type'    => $pg['post_type'],
					'post_status'  => 'draft',
					'post_title'   => $pg['h1'],
					'post_name'    => $slug,
					'post_parent'  => $parent,
					'post_content' => $pg['content_blocks'],
					'post_author'  => ! empty( $ctx['bundle']['settings']['author_id'] ) ? (int) $ctx['bundle']['settings']['author_id'] : get_current_user_id(),
				)
			),
			true
		);
		if ( is_wp_error( $id ) ) {
			cms_exec_issue( $ctx, 'error', $pg['id'], 'create failed: ' . $id->get_error_message() );
			return;
		}
		update_post_meta( $id, '_cms_handoff', $ctx['client'] . ':' . $pg['id'] );
		cms_exec_log( $ctx, array( 'type' => 'created', 'page' => $pg['id'], 'post' => $id ) );
		$ctx['sum']['created']++;
		cms_exec_seo( $ctx, $id, $pg );
		if ( ! empty( $pg['noindex'] ) ) {
			cms_exec_set_meta( $ctx, $id, $pg['id'], '_seopress_robots_index', 'yes' );
		}
		$ctx['issues'][] = array( 'level' => 'info', 'page' => $pg['id'], 'msg' => 'draft created: ' . admin_url( 'post.php?post=' . $id . '&action=edit' ) );
	}

	function cms_exec_stage_preview( &$ctx, $pg ) {
		$t = cms_exec_target( $ctx, $pg );
		if ( ! $t ) {
			cms_exec_issue( $ctx, 'error', $pg['id'], 'target page not found' );
			return;
		}
		if ( cms_exec_staged( $ctx, $pg, '_cms_preview_for' ) ) {
			$ctx['sum']['unchanged']++;
			return;
		}
		$id = wp_insert_post(
			wp_slash(
				array(
					'post_type'    => $t->post_type,
					'post_status'  => 'draft',
					'post_title'   => 'PREVIEW – ' . $pg['h1'],
					'post_name'    => 'cms-preview-' . sanitize_title( $pg['id'] ),
					'post_content' => $pg['content_blocks'],
				)
			),
			true
		);
		if ( is_wp_error( $id ) ) {
			cms_exec_issue( $ctx, 'error', $pg['id'], 'preview failed: ' . $id->get_error_message() );
			return;
		}
		update_post_meta( $id, '_cms_preview_for', $ctx['client'] . ':' . $pg['id'] );
		update_post_meta( $id, '_cms_preview_target', $t->ID );
		update_post_meta( $id, '_seopress_robots_index', 'yes' );
		cms_exec_log( $ctx, array( 'type' => 'created', 'page' => $pg['id'], 'post' => $id, 'preview_for' => $t->ID ) );
		$ctx['sum']['created']++;
		$ctx['issues'][] = array( 'level' => 'info', 'page' => $pg['id'], 'msg' => 'preview draft for post ' . $t->ID . ': ' . admin_url( 'post.php?post=' . $id . '&action=edit' ) );
	}

	/* ------------------------------------------------------------------ */
	/* APPLY phase "pages" (chunked)                                       */
	/* ------------------------------------------------------------------ */

	function cms_exec_apply_pages( &$ctx, $opts ) {
		$pages  = $ctx['bundle']['pages'];
		$offset = isset( $opts['offset'] ) ? max( 0, (int) $opts['offset'] ) : 0;
		$total  = count( $pages );
		for ( $i = $offset; $i < $total; $i++ ) {
			if ( cms_exec_out_of_time( $ctx ) ) {
				$ctx['next_offset'] = $i;
				$ctx['next_step']   = 'run apply phase=pages again with offset=' . $i . ' and the same run_id';
				return;
			}
			cms_exec_apply_page( $ctx, $pages[ $i ] );
		}
		$ctx['next_step'] = 'pages done: run apply with phase=site and the same run_id';
	}

	function cms_exec_apply_page( &$ctx, $pg ) {
		if ( 'create' === $pg['action'] ) {
			$p = cms_exec_staged( $ctx, $pg, '_cms_handoff' );
			if ( ! $p ) {
				cms_exec_issue( $ctx, 'error', $pg['id'], 'no staged draft: run stage first' );
				return;
			}
			cms_exec_seo( $ctx, $p->ID, $pg );
			if ( 'publish' !== $p->post_status ) {
				cms_exec_set_field( $ctx, $p->ID, $pg['id'], 'post_status', 'publish' );
				$slug = get_post_field( 'post_name', $p->ID );
				if ( basename( cms_exec_path( $pg['url'] ) ) !== $slug ) {
					cms_exec_issue( $ctx, 'error', $pg['id'], 'published with slug ' . $slug . ' instead of the handoff slug: fix by hand (URL-04)' );
				}
			}
			cms_exec_rocket( $p->ID );
			return;
		}

		$t = cms_exec_target( $ctx, $pg );
		if ( ! $t ) {
			cms_exec_issue( $ctx, 'error', $pg['id'], 'target not found at ' . $pg['url'] );
			return;
		}

		if ( 'build' === $pg['route'] ) {
			$prev = cms_exec_staged( $ctx, $pg, '_cms_preview_for' );
			if ( ! $prev ) {
				cms_exec_issue( $ctx, 'error', $pg['id'], 'no preview draft: run stage first' );
				return;
			}
			// The preview is the reviewed (and possibly VA-styled) version: it wins over the bundle.
			if ( cms_exec_set_content( $ctx, $t->ID, $pg['id'], get_post_field( 'post_content', $prev->ID ) ) ) {
				wp_trash_post( $prev->ID );
				cms_exec_log( $ctx, array( 'type' => 'trashed_preview', 'page' => $pg['id'], 'post' => $prev->ID ) );
			}
		}

		cms_exec_seo( $ctx, $t->ID, $pg );
		cms_exec_set_h1( $ctx, $t, $pg );
		if ( isset( $pg['noindex'] ) ) {
			cms_exec_set_meta( $ctx, $t->ID, $pg['id'], '_seopress_robots_index', $pg['noindex'] ? 'yes' : '' );
		}
		// Existing draft that this handoff publishes (e.g. drafts created earlier).
		if ( ! empty( $pg['publish'] ) && 'publish' !== get_post_status( $t->ID ) ) {
			$want = basename( cms_exec_path( $pg['url'] ) );
			if ( get_post_field( 'post_name', $t->ID ) !== $want ) {
				cms_exec_issue( $ctx, 'error', $pg['id'], 'draft slug is "' . get_post_field( 'post_name', $t->ID ) . '", handoff url needs "' . $want . '": not published' );
			} else {
				cms_exec_set_field( $ctx, $t->ID, $pg['id'], 'post_status', 'publish' );
			}
		}
		cms_exec_rocket( $t->ID );
	}

	function cms_exec_rocket( $pid ) {
		if ( function_exists( 'rocket_clean_post' ) ) {
			rocket_clean_post( $pid );
		}
	}

	/* ------------------------------------------------------------------ */
	/* APPLY phase "site": noindex list, redirects, link updates           */
	/* ------------------------------------------------------------------ */

	function cms_exec_apply_site( &$ctx ) {
		$b = $ctx['bundle'];

		foreach ( $b['noindex'] as $n ) {
			$p = cms_exec_find( $n['url'] );
			if ( ! $p ) {
				cms_exec_issue( $ctx, 'error', $n['url'], 'noindex: page not found' );
				continue;
			}
			cms_exec_set_meta( $ctx, $p->ID, $n['url'], '_seopress_robots_index', 'yes' );
			cms_exec_rocket( $p->ID );
		}

		$engine = cms_exec_redirect_engine();
		foreach ( $b['redirects'] as $r ) {
			if ( cms_exec_out_of_time( $ctx ) ) {
				$ctx['next_step'] = 'out of time: run apply phase=site again with the same run_id (finished items are skipped)';
				return;
			}
			cms_exec_redirect( $ctx, $engine, $r );
		}

		foreach ( $b['link_updates'] as $lu ) {
			if ( cms_exec_out_of_time( $ctx ) ) {
				$ctx['next_step'] = 'out of time: run apply phase=site again with the same run_id';
				return;
			}
			cms_exec_link_update( $ctx, $lu );
		}

		if ( function_exists( 'rocket_clean_domain' ) && $ctx['sum']['changed'] > 0 && ! empty( $b['link_updates'] ) ) {
			rocket_clean_domain();
		}
		$ctx['next_step'] = 'apply complete: run verify, then verify_live.py';
	}

	function cms_exec_rel( $url ) {
		$p = wp_parse_url( $url, PHP_URL_PATH );
		$p = $p ? $p : '/';
		return '/' . ltrim( $p, '/' );
	}

	function cms_exec_redirect_engine() {
		if ( class_exists( 'Red_Item' ) ) {
			return 'redirection';
		}
		if ( defined( 'SEOPRESS_PRO_VERSION' ) ) {
			return 'seopress_pro';
		}
		return '';
	}

	function cms_exec_redirect_lookup( $engine, $from ) {
		global $wpdb;
		$from = cms_exec_rel( $from );
		$alts = array_unique( array( $from, untrailingslashit( $from ), trailingslashit( $from ) ) );
		if ( 'redirection' === $engine ) {
			foreach ( $alts as $a ) {
				$row = $wpdb->get_row( $wpdb->prepare( "SELECT id, action_data FROM {$wpdb->prefix}redirection_items WHERE url = %s AND status = 'enabled' LIMIT 1", $a ), ARRAY_A );
				if ( $row ) {
					return array( 'id' => (int) $row['id'], 'to' => cms_exec_rel( $row['action_data'] ) );
				}
			}
		} elseif ( 'seopress_pro' === $engine ) {
			foreach ( $alts as $a ) {
				$ids = get_posts( array( 'post_type' => 'seopress_404', 'post_status' => 'any', 'title' => ltrim( $a, '/' ), 'posts_per_page' => 1, 'fields' => 'ids' ) );
				if ( $ids ) {
					return array( 'id' => (int) $ids[0], 'to' => cms_exec_rel( get_post_meta( $ids[0], '_seopress_redirections_value', true ) ) );
				}
			}
		}
		return null;
	}

	function cms_exec_redirect( &$ctx, $engine, $r ) {
		global $wpdb;
		$from = cms_exec_rel( $r['from'] );
		$to   = cms_exec_rel( $r['to'] );
		$code = isset( $r['type'] ) ? (int) $r['type'] : 301;

		$existing = cms_exec_redirect_lookup( $engine, $from );
		if ( $existing ) {
			if ( untrailingslashit( $existing['to'] ) === untrailingslashit( $to ) ) {
				$ctx['sum']['unchanged']++;
			} else {
				cms_exec_issue( $ctx, 'error', $from, 'existing redirect to ' . $existing['to'] . ' left untouched (handoff says ' . $to . ')' );
				return;
			}
		} elseif ( 'redirection' === $engine ) {
			$gid  = (int) $wpdb->get_var( "SELECT id FROM {$wpdb->prefix}redirection_groups WHERE status = 'enabled' ORDER BY id ASC LIMIT 1" );
			$item = Red_Item::create(
				array(
					'url'         => $from,
					'action_data' => array( 'url' => $to ),
					'regex'       => false,
					'group_id'    => $gid ? $gid : 1,
					'match_type'  => 'url',
					'action_type' => 'url',
					'action_code' => $code,
				)
			);
			if ( is_wp_error( $item ) ) {
				cms_exec_issue( $ctx, 'error', $from, 'redirect failed: ' . $item->get_error_message() );
				return;
			}
			cms_exec_log( $ctx, array( 'type' => 'redirect_created', 'engine' => $engine, 'id' => (int) $item->get_id(), 'from' => $from, 'to' => $to ) );
			$ctx['sum']['created']++;
		} elseif ( 'seopress_pro' === $engine ) {
			$id = wp_insert_post( array( 'post_type' => 'seopress_404', 'post_status' => 'publish', 'post_title' => ltrim( $from, '/' ) ), true );
			if ( is_wp_error( $id ) ) {
				cms_exec_issue( $ctx, 'error', $from, 'redirect failed: ' . $id->get_error_message() );
				return;
			}
			update_post_meta( $id, '_seopress_redirections_enabled', 'yes' );
			update_post_meta( $id, '_seopress_redirections_type', $code );
			update_post_meta( $id, '_seopress_redirections_value', home_url( $to ) );
			cms_exec_log( $ctx, array( 'type' => 'redirect_created', 'engine' => $engine, 'id' => (int) $id, 'from' => $from, 'to' => $to ) );
			$ctx['sum']['created']++;
			cms_exec_issue( $ctx, 'warning', $from, 'SEOPress Pro redirect created: confirm it fires (first-use check)' );
		} else {
			cms_exec_issue( $ctx, 'error', $from, 'no redirect engine' );
			return;
		}

		// RDR-04: repoint any existing redirect that targeted the now-redirected URL.
		if ( 'redirection' === $engine ) {
			$chains = $wpdb->get_results( $wpdb->prepare( "SELECT id, action_data FROM {$wpdb->prefix}redirection_items WHERE action_data IN (%s, %s, %s)", $from, untrailingslashit( $from ), home_url( $from ) ), ARRAY_A );
			foreach ( $chains as $c ) {
				$wpdb->update( $wpdb->prefix . 'redirection_items', array( 'action_data' => $to ), array( 'id' => (int) $c['id'] ) );
				cms_exec_log( $ctx, array( 'type' => 'redirect_repointed', 'id' => (int) $c['id'], 'old' => $c['action_data'], 'new' => $to ) );
				$ctx['sum']['changed']++;
			}
		}

		// Retire the source page (draft) so it leaves the sitemap; content is kept.
		if ( ! isset( $r['retire_source'] ) || $r['retire_source'] ) {
			$src = cms_exec_find( $from );
			if ( $src && 'publish' === $src->post_status && (int) get_option( 'page_on_front' ) !== $src->ID ) {
				cms_exec_set_field( $ctx, $src->ID, $from, 'post_status', 'draft' );
			}
		}
	}

	/** RDR-05: point internal links straight at the destination. */
	function cms_exec_link_update( &$ctx, $lu ) {
		global $wpdb;
		$old  = cms_exec_rel( $lu['old_url'] );
		$new  = cms_exec_rel( $lu['new_url'] );
		$home = untrailingslashit( home_url() );
		$pairs = array();
		foreach ( array_unique( array( trailingslashit( $old ), untrailingslashit( $old ) ) ) as $o ) {
			$pairs[ 'href="' . $o . '"' ]         = 'href="' . $new . '"';
			$pairs[ 'href="' . $home . $o . '"' ] = 'href="' . $home . $new . '"';
		}
		$like = '%' . $wpdb->esc_like( untrailingslashit( $old ) ) . '%';
		$ids  = $wpdb->get_col( $wpdb->prepare( "SELECT ID FROM {$wpdb->posts} WHERE post_status = 'publish' AND post_type NOT IN ('revision','nav_menu_item','attachment') AND post_content LIKE %s", $like ) );
		foreach ( $ids as $pid ) {
			$c  = get_post_field( 'post_content', $pid );
			$nc = strtr( $c, $pairs );
			if ( $nc !== $c ) {
				cms_exec_set_content( $ctx, (int) $pid, 'links:' . $old, $nc );
				cms_exec_rocket( (int) $pid );
			}
		}
	}

	/* ------------------------------------------------------------------ */
	/* VERIFY (read-only): database values vs bundle                       */
	/* ------------------------------------------------------------------ */

	function cms_exec_verify( &$ctx ) {
		foreach ( $ctx['bundle']['pages'] as $pg ) {
			$p = ( 'create' === $pg['action'] ) ? cms_exec_staged( $ctx, $pg, '_cms_handoff' ) : cms_exec_target( $ctx, $pg );
			if ( ! $p ) {
				cms_exec_issue( $ctx, 'error', $pg['id'], 'page not found' );
				continue;
			}
			$checks = array(
				'seo_title'        => array( get_post_meta( $p->ID, '_seopress_titles_title', true ), isset( $pg['seo_title'] ) ? $pg['seo_title'] : null ),
				'meta_description' => array( get_post_meta( $p->ID, '_seopress_titles_desc', true ), isset( $pg['meta_description'] ) ? preg_replace( '/\s+/', ' ', $pg['meta_description'] ) : null ),
			);
			foreach ( $checks as $k => $pair ) {
				if ( null !== $pair[1] && (string) $pair[0] !== (string) $pair[1] ) {
					cms_exec_issue( $ctx, 'error', $pg['id'], $k . ' mismatch: "' . $pair[0] . '"' );
				}
			}
			if ( 'publish' !== $p->post_status ) {
				cms_exec_issue( $ctx, 'error', $pg['id'], 'status is ' . $p->post_status );
			}
			if ( ! empty( $pg['h1'] ) ) {
				$mode = cms_exec_h1_mode( $p );
				$have = ( 'title' === $mode ) ? $p->post_title : ( preg_match( '#<h1\b[^>]*>(.*?)</h1>#is', $p->post_content, $m ) ? wp_strip_all_tags( $m[1] ) : '' );
				if ( html_entity_decode( $have ) !== $pg['h1'] ) {
					cms_exec_issue( $ctx, 'error', $pg['id'], 'H1 mismatch (' . $mode . '): "' . $have . '"' );
				}
			}
			$ctx['sum']['unchanged']++;
		}
		$engine = cms_exec_redirect_engine();
		foreach ( $ctx['bundle']['redirects'] as $r ) {
			$e = cms_exec_redirect_lookup( $engine, $r['from'] );
			if ( ! $e || untrailingslashit( $e['to'] ) !== untrailingslashit( cms_exec_rel( $r['to'] ) ) ) {
				cms_exec_issue( $ctx, 'error', $r['from'], 'redirect missing or wrong target' );
			}
		}
	}

	/* ------------------------------------------------------------------ */
	/* ROLLBACK a run from its log                                         */
	/* ------------------------------------------------------------------ */

	function cms_exec_rollback( &$ctx ) {
		global $wpdb;
		$f = cms_exec_dir( $ctx['client'] ) . '/logs/' . $ctx['run_id'] . '.jsonl';
		if ( ! file_exists( $f ) ) {
			cms_exec_issue( $ctx, 'error', '-', 'no log for run ' . $ctx['run_id'] );
			return;
		}
		$lines = array_reverse( array_filter( explode( "\n", file_get_contents( $f ) ) ) );
		foreach ( $lines as $line ) {
			$e = json_decode( $line, true );
			if ( ! $e ) {
				continue;
			}
			switch ( $e['type'] ) {
				case 'meta':
					if ( '' === $e['old'] ) {
						delete_post_meta( $e['post'], $e['key'] );
					} else {
						update_post_meta( $e['post'], $e['key'], $e['old'] );
					}
					break;
				case 'field':
					wp_update_post( wp_slash( array( 'ID' => $e['post'], $e['key'] => $e['old'] ) ) );
					break;
				case 'content':
					if ( ! empty( $e['revision'] ) ) {
						wp_restore_post_revision( $e['revision'] );
					} else {
						cms_exec_issue( $ctx, 'warning', $e['page'], 'no revision saved for post ' . $e['post'] . ': restore content from backup' );
					}
					break;
				case 'created':
					wp_trash_post( $e['post'] );
					break;
				case 'trashed_preview':
					wp_untrash_post( $e['post'] );
					break;
				case 'redirect_created':
					if ( 'redirection' === $e['engine'] ) {
						$wpdb->delete( $wpdb->prefix . 'redirection_items', array( 'id' => (int) $e['id'] ) );
					} else {
						wp_trash_post( (int) $e['id'] );
					}
					break;
				case 'redirect_repointed':
					$wpdb->update( $wpdb->prefix . 'redirection_items', array( 'action_data' => $e['old'] ), array( 'id' => (int) $e['id'] ) );
					break;
			}
			$ctx['sum']['changed']++;
		}
		if ( function_exists( 'rocket_clean_domain' ) ) {
			rocket_clean_domain();
		}
		rename( $f, $f . '.rolled-back' );
	}
}
