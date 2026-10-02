#!/usr/bin/env node
/**
 * md-to-docx.js — one converter for every deliverable in this plugin.
 *
 *   node md-to-docx.js input.md output.docx
 *
 * Supported markdown:
 *   # .. ###### headings
 *   paragraphs
 *   - / * bullets (2-space indent = nested level, up to 3 levels)
 *   1. numbered lists (each list restarts at 1)
 *   | pipe | tables | with a |---|---| separator row
 *   > Note: / > Stop: / > Rule: / plain > blockquote callouts
 *   ```fenced code blocks```
 *   === on its own line = page break
 *   ---  on its own line = horizontal rule
 *   inline **bold**, *italic*, _italic_, `code`, [text](url)
 *
 * Deliberately NOT supported: images, footnotes, nested tables, HTML.
 * If a deliverable needs one of those, the deliverable is wrong, not the script.
 */

const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, BorderStyle, ShadingType,
  PageBreak, ExternalHyperlink, LevelFormat, convertInchesToTwip,
} = require("docx");

// ---------------------------------------------------------------- constants
const PAGE_W = 12240;              // US Letter, DXA
const PAGE_H = 15840;
const MARGIN = 1080;               // 0.75"
const CONTENT_W = PAGE_W - MARGIN * 2;

const FONT = "Calibri";
const MONO = "Consolas";

const CALLOUT_STYLES = {
  stop: { fill: "FCE8E6", accent: "C5221F" },
  rule: { fill: "E8F0FE", accent: "1A73E8" },
  note: { fill: "F1F3F4", accent: "5F6368" },
  plain: { fill: "F1F3F4", accent: "9AA0A6" },
};

// ------------------------------------------------------------ inline parsing
// Order matters: code first so ** inside `code` is left alone.
const INLINE = /(`[^`]+`)|(\[[^\]]+\]\([^)]+\))|(\*\*[^*]+\*\*)|(\*[^*\n]+\*)|(_[^_\n]+_)/;

function inlineRuns(text, base = {}) {
  const runs = [];
  let rest = text;

  while (rest.length) {
    const m = rest.match(INLINE);
    if (!m) {
      if (rest) runs.push(new TextRun({ text: rest, font: FONT, ...base }));
      break;
    }
    if (m.index > 0) {
      runs.push(new TextRun({ text: rest.slice(0, m.index), font: FONT, ...base }));
    }
    const tok = m[0];

    if (tok.startsWith("`")) {
      runs.push(new TextRun({
        text: tok.slice(1, -1), font: MONO, size: 19,
        shading: { type: ShadingType.CLEAR, fill: "F1F3F4" }, ...base,
      }));
    } else if (tok.startsWith("[")) {
      const label = tok.slice(1, tok.indexOf("]"));
      const href = tok.slice(tok.indexOf("(") + 1, -1);
      runs.push(new ExternalHyperlink({
        link: href,
        children: [new TextRun({ text: label, font: FONT, color: "1A73E8", underline: {}, ...base })],
      }));
    } else if (tok.startsWith("**")) {
      runs.push(...inlineRuns(tok.slice(2, -2), { ...base, bold: true }));
    } else {
      runs.push(...inlineRuns(tok.slice(1, -1), { ...base, italics: true }));
    }
    rest = rest.slice(m.index + tok.length);
  }
  return runs.length ? runs : [new TextRun({ text: "", font: FONT })];
}

// ------------------------------------------------------------- block parsing
function isTableRow(l) { return /^\s*\|.*\|\s*$/.test(l); }
function isTableSep(l) { return /^\s*\|[\s:|-]+\|\s*$/.test(l) && l.includes("-"); }
function splitRow(l) {
  return l.trim().replace(/^\|/, "").replace(/\|$/, "").split("|").map(c => c.trim());
}

function parse(md) {
  const lines = md.replace(/\r\n/g, "\n").split("\n");
  const blocks = [];
  let i = 0;
  let olCount = 0;

  while (i < lines.length) {
    const line = lines[i];
    const t = line.trim();

    if (!t) { i++; continue; }

    // page break / rule
    if (/^={3,}$/.test(t)) { blocks.push({ type: "pagebreak" }); i++; continue; }
    if (/^(-{3,}|\*{3,}|_{3,})$/.test(t)) { blocks.push({ type: "hr" }); i++; continue; }

    // front matter fence at the very top — skip it
    if (i === 0 && t === "---") {
      let j = i + 1;
      while (j < lines.length && lines[j].trim() !== "---") j++;
      i = j + 1;
      continue;
    }

    // fenced code
    if (t.startsWith("```")) {
      const body = [];
      i++;
      while (i < lines.length && !lines[i].trim().startsWith("```")) body.push(lines[i++]);
      i++;
      blocks.push({ type: "code", lines: body });
      continue;
    }

    // heading
    const h = t.match(/^(#{1,6})\s+(.*)$/);
    if (h) { blocks.push({ type: "heading", level: h[1].length, text: h[2].trim() }); i++; continue; }

    // table
    if (isTableRow(line) && i + 1 < lines.length && isTableSep(lines[i + 1])) {
      const header = splitRow(lines[i]);
      i += 2;
      const rows = [];
      while (i < lines.length && isTableRow(lines[i])) rows.push(splitRow(lines[i++]));
      blocks.push({ type: "table", header, rows });
      continue;
    }

    // blockquote / callout
    if (/^>\s?/.test(t)) {
      const buf = [];
      while (i < lines.length && /^\s*>\s?/.test(lines[i])) {
        buf.push(lines[i].replace(/^\s*>\s?/, ""));
        i++;
      }
      const text = buf.join(" ").replace(/\s+/g, " ").trim();
      const lm = text.match(/^(Stop|Rule|Note|Warning|Caution):\s*(.*)$/i);
      let kind = "plain", label = null, body = text;
      if (lm) {
        label = lm[1];
        body = lm[2];
        const k = label.toLowerCase();
        kind = k === "stop" || k === "warning" || k === "caution" ? "stop"
             : k === "rule" ? "rule" : "note";
      }
      blocks.push({ type: "callout", kind, label, text: body });
      continue;
    }

    // bullet list
    if (/^\s*[-*+]\s+/.test(line)) {
      const items = [];
      while (i < lines.length && /^\s*[-*+]\s+/.test(lines[i])) {
        const indent = lines[i].match(/^\s*/)[0].replace(/\t/g, "  ").length;
        let text = lines[i].replace(/^\s*[-*+]\s+/, "");
        i++;
        // continuation lines (wrapped source)
        while (i < lines.length && lines[i].trim() &&
               !/^\s*([-*+]|\d+\.)\s+/.test(lines[i]) &&
               !/^\s*[>#|`]/.test(lines[i]) &&
               lines[i].match(/^\s*/)[0].length > indent) {
          text += " " + lines[i].trim();
          i++;
        }
        items.push({ level: Math.min(Math.floor(indent / 2), 2), text });
      }
      blocks.push({ type: "ul", items });
      continue;
    }

    // numbered list
    if (/^\s*\d+\.\s+/.test(line)) {
      const items = [];
      while (i < lines.length && /^\s*\d+\.\s+/.test(lines[i])) {
        const indent = lines[i].match(/^\s*/)[0].replace(/\t/g, "  ").length;
        let text = lines[i].replace(/^\s*\d+\.\s+/, "");
        i++;
        while (i < lines.length && lines[i].trim() &&
               !/^\s*([-*+]|\d+\.)\s+/.test(lines[i]) &&
               !/^\s*[>#|`]/.test(lines[i]) &&
               lines[i].match(/^\s*/)[0].length > indent) {
          text += " " + lines[i].trim();
          i++;
        }
        items.push({ level: Math.min(Math.floor(indent / 3), 2), text });
      }
      blocks.push({ type: "ol", items, ref: `ol-${olCount++}` });
      continue;
    }

    // paragraph
    const buf = [];
    while (i < lines.length && lines[i].trim() &&
           !/^\s*([-*+]|\d+\.)\s+/.test(lines[i]) &&
           !/^\s*[>#]/.test(lines[i]) &&
           !isTableRow(lines[i]) &&
           !/^\s*```/.test(lines[i]) &&
           !/^\s*(={3,}|-{3,})\s*$/.test(lines[i])) {
      buf.push(lines[i].trim());
      i++;
    }
    blocks.push({ type: "p", text: buf.join(" ") });
  }

  return { blocks, olCount };
}

// -------------------------------------------------------------- doc building
const HEADINGS = [
  HeadingLevel.HEADING_1, HeadingLevel.HEADING_2, HeadingLevel.HEADING_3,
  HeadingLevel.HEADING_4, HeadingLevel.HEADING_5, HeadingLevel.HEADING_6,
];

function columnWidths(header, rows) {
  const n = header.length;
  const score = header.map((h, c) => {
    let max = h.length;
    for (const r of rows) max = Math.max(max, (r[c] || "").length);
    return Math.max(6, Math.min(max, 60));
  });
  const total = score.reduce((a, b) => a + b, 0);
  const widths = score.map(s => Math.floor((s / total) * CONTENT_W));
  widths[n - 1] = CONTENT_W - widths.slice(0, n - 1).reduce((a, b) => a + b, 0);
  return widths;
}

function buildTable(b) {
  const widths = columnWidths(b.header, b.rows);
  const cell = (text, c, isHeader) => new TableCell({
    width: { size: widths[c], type: WidthType.DXA },
    shading: isHeader ? { type: ShadingType.CLEAR, fill: "E8EAED" } : undefined,
    margins: { top: 60, bottom: 60, left: 110, right: 110 },
    children: [new Paragraph({
      spacing: { before: 0, after: 0 },
      children: inlineRuns(text || "", isHeader ? { bold: true } : {}),
    })],
  });

  return new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: widths,
    rows: [
      new TableRow({ tableHeader: true, children: b.header.map((h, c) => cell(h, c, true)) }),
      ...b.rows.map(r => new TableRow({
        children: b.header.map((_, c) => cell(r[c], c, false)),
      })),
    ],
  });
}

function buildCallout(b) {
  const s = CALLOUT_STYLES[b.kind];
  const children = [];
  if (b.label) children.push(new TextRun({ text: `${b.label}: `, font: FONT, bold: true, color: s.accent }));
  children.push(...inlineRuns(b.text));

  return new Paragraph({
    children,
    spacing: { before: 160, after: 160 },
    indent: { left: 180 },
    shading: { type: ShadingType.CLEAR, fill: s.fill },
    border: {
      left: { style: BorderStyle.SINGLE, size: 18, space: 10, color: s.accent },
      top: { style: BorderStyle.SINGLE, size: 2, space: 6, color: s.fill },
      bottom: { style: BorderStyle.SINGLE, size: 2, space: 6, color: s.fill },
      right: { style: BorderStyle.SINGLE, size: 2, space: 6, color: s.fill },
    },
  });
}

function build(blocks) {
  const out = [];
  for (const b of blocks) {
    switch (b.type) {
      case "pagebreak":
        out.push(new Paragraph({ children: [new PageBreak()] }));
        break;

      case "hr":
        out.push(new Paragraph({
          spacing: { before: 120, after: 120 },
          border: { bottom: { style: BorderStyle.SINGLE, size: 6, space: 1, color: "D0D3D6" } },
          children: [new TextRun({ text: "", font: FONT })],
        }));
        break;

      case "heading":
        out.push(new Paragraph({
          heading: HEADINGS[b.level - 1],
          spacing: { before: b.level === 1 ? 240 : 220, after: 100 },
          keepNext: true,
          children: inlineRuns(b.text),
        }));
        break;

      case "p":
        out.push(new Paragraph({
          spacing: { after: 140, line: 276 },
          children: inlineRuns(b.text),
        }));
        break;

      case "ul":
        for (const [idx, it] of b.items.entries()) {
          out.push(new Paragraph({
            numbering: { reference: "bullets", level: it.level },
            spacing: { before: idx === 0 ? 120 : 0, after: 60, line: 276 },
            children: inlineRuns(it.text),
          }));
        }
        break;

      case "ol":
        for (const [idx, it] of b.items.entries()) {
          out.push(new Paragraph({
            numbering: { reference: b.ref, level: it.level },
            spacing: { before: idx === 0 ? 120 : 0, after: 60, line: 276 },
            children: inlineRuns(it.text),
          }));
        }
        break;

      case "callout":
        out.push(buildCallout(b));
        break;

      case "code":
        for (const l of b.lines) {
          out.push(new Paragraph({
            spacing: { before: 0, after: 0 },
            indent: { left: 240 },
            shading: { type: ShadingType.CLEAR, fill: "F1F3F4" },
            children: [new TextRun({ text: l || " ", font: MONO, size: 19 })],
          }));
        }
        out.push(new Paragraph({ spacing: { after: 120 }, children: [new TextRun({ text: "", font: FONT })] }));
        break;

      case "table":
        out.push(buildTable(b));
        out.push(new Paragraph({ spacing: { after: 160 }, children: [new TextRun({ text: "", font: FONT })] }));
        break;
    }
  }
  return out;
}

function numberingConfig(olCount) {
  const configs = [{
    reference: "bullets",
    levels: [0, 1, 2].map(l => ({
      level: l,
      format: LevelFormat.BULLET,
      text: ["\u25CF", "\u25CB", "\u25AA"][l],
      alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: convertInchesToTwip(0.3 + l * 0.25), hanging: 220 } } },
    })),
  }];

  for (let n = 0; n < olCount; n++) {
    configs.push({
      reference: `ol-${n}`,
      levels: [0, 1, 2].map(l => ({
        level: l,
        format: [LevelFormat.DECIMAL, LevelFormat.LOWER_LETTER, LevelFormat.LOWER_ROMAN][l],
        text: `%${l + 1}.`,
        alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: convertInchesToTwip(0.35 + l * 0.25), hanging: 260 } } },
      })),
    });
  }
  return { config: configs };
}

// ---------------------------------------------------------------------- main
function main() {
  const [input, output] = process.argv.slice(2);
  if (!input) {
    console.error("usage: node md-to-docx.js <input.md> [output.docx]");
    process.exit(1);
  }
  const outPath = output || input.replace(/\.md$/i, "") + ".docx";

  const md = fs.readFileSync(input, "utf8");
  const { blocks, olCount } = parse(md);

  const doc = new Document({
    numbering: numberingConfig(olCount),
    styles: {
      default: {
        document: { run: { font: FONT, size: 22 } },
      },
      paragraphStyles: [
        { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
          run: { font: FONT, size: 34, bold: true, color: "16324F" } },
        { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
          run: { font: FONT, size: 27, bold: true, color: "16324F" } },
        { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
          run: { font: FONT, size: 23, bold: true, color: "2B5070" } },
        { id: "Heading4", name: "Heading 4", basedOn: "Normal", next: "Normal", quickFormat: true,
          run: { font: FONT, size: 22, bold: true, color: "3C3C3C" } },
        { id: "Heading5", name: "Heading 5", basedOn: "Normal", next: "Normal", quickFormat: true,
          run: { font: FONT, size: 22, bold: true, italics: true, color: "3C3C3C" } },
        { id: "Heading6", name: "Heading 6", basedOn: "Normal", next: "Normal", quickFormat: true,
          run: { font: FONT, size: 21, bold: true, color: "5F6368" } },
      ],
    },
    sections: [{
      properties: {
        page: {
          size: { width: PAGE_W, height: PAGE_H },
          margin: { top: MARGIN, right: MARGIN, bottom: MARGIN, left: MARGIN },
        },
      },
      children: build(blocks),
    }],
  });

  Packer.toBuffer(doc).then(buf => {
    fs.writeFileSync(outPath, buf);
    console.log(`${path.basename(input)} -> ${outPath}  (${blocks.length} blocks)`);
  }).catch(err => {
    console.error("conversion failed:", err.message);
    process.exit(1);
  });
}

main();
