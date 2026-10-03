<?php
/**
 * Plugin Name: seo-ops head meta (must-use)
 * Description: Exposes the Kadence per-page head-code field to the REST API so seo-ops (scripts/wp.py set-head)
 *              can read and write page schema. Install in wp-content/mu-plugins/ on the client site.
 * Version: 0.1 — key filled in during the WordPress pilot.
 *
 * PILOT STEP: run `python3 scripts/wp.py inspect <slug> <url>` on a page whose head field is set in the
 * Kadence UI, find the meta key that holds it, put it below AND in config.json "kadence_head_meta_key".
 * Until both are set, wp.py refuses set-head and schema goes out as a VA handoff.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

const SEO_OPS_HEAD_META_KEY = ''; // e.g. '_kad_post_head_code' — confirm on the pilot site; never guess.

add_action( 'init', function () {
	if ( SEO_OPS_HEAD_META_KEY === '' ) {
		return; // not configured yet: expose nothing
	}
	foreach ( array( 'page', 'post' ) as $type ) {
		register_post_meta( $type, SEO_OPS_HEAD_META_KEY, array(
			'type'          => 'string',
			'single'        => true,
			'show_in_rest'  => true,
			'auth_callback' => function () { return current_user_can( 'edit_posts' ); },
		) );
	}
} );
