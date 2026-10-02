#!/usr/bin/env node
/**
 * render_proof_sheet.js — turn an intake record into a client-facing .docx proof sheet.
 *
 *   node render_proof_sheet.js <record.yaml> [output.docx]
 *
 * Produces the three-block structure defined in references/proof-sheet.md.
 * Upload the result to Google Drive and share with comment access.
 *
 * Requires: docx (preinstalled). YAML records also need js-yaml — "npm install js-yaml".
 * A .json record with the same shape works with no extra dependency.
 */

const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  WidthType, ShadingType, AlignmentType, HeadingLevel, BorderStyle,
} = require("docx");

// ---------- config ----------
const PAGE = { width: 12240, height: 15840 };      // US Letter, DXA
const CONTENT_W = 9360;                             // 6.5in usable
const COLS_A = [4200, 1200, 3960];
const COLS_B = [6000, 3360];
const COLS_ACCESS = [3600, 3000, 2760];
const INK = "1A1A1A";
const MUTED = "6B6B6B";
const BAND = "EFEFEF";
const FLAG = "FFF4E5";

// ---------- record loading ----------
function loadRecord(p) {
  const raw = fs.readFileSync(p, "utf8");
  if (p.endsWith(".json")) return JSON.parse(raw);
  try {
    return require("js-yaml").load(raw);
  } catch (e) {
    console.error(
      "Could not parse YAML. Install js-yaml (npm i js-yaml) or pass a .json record."
    );
    throw e;
  }
}

// ---------- small helpers ----------
const val = (f) => (f && f.value != null && f.value !== "" ? String(f.value) : "");
const src = (f) => (f && f.source ? String(f.source) : "");

function p(text, opts = {}) {
  return new Paragraph({
    spacing: { before: opts.before ?? 0, after: opts.after ?? 80 },
    alignment: opts.align,
    children: [
      new TextRun({
        text: text ?? "",
        bold: opts.bold,
        italics: opts.italic,
        size: opts.size ?? 20,
        color: opts.color ?? INK,
        font: "Calibri",
      }),
    ],
  });
}

function cellPara(text, source, opts = {}) {
  const kids = [
    new TextRun({
      text: text ?? "",
      bold: opts.bold,
      size: opts.size ?? 20,
      color: opts.color ?? INK,
      font: "Calibri",
    }),
  ];
  if (source) {
    kids.push(
      new TextRun({
        text: `  (${source})`,
        italics: true,
        size: 16,
        color: MUTED,
        font: "Calibri",
      })
    );
  }
  return new Paragraph({ spacing: { before: 40, after: 40 }, children: kids });
}

function cell(children, width, shading) {
  return new TableCell({
    width: { size: width, type: WidthType.DXA },
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    shading: shading
      ? { type: ShadingType.CLEAR, fill: shading, color: "auto" }
      : undefined,
    children: Array.isArray(children) ? children : [children],
  });
}

function table(rows, widths) {
  return new Table({
    columnWidths: widths,
    width: { size: widths.reduce((a, b) => a + b, 0), type: WidthType.DXA },
    rows,
  });
}

function headerRow(labels, widths) {
  return new TableRow({
    tableHeader: true,
    children: labels.map((l, i) =>
      cell(cellPara(l, null, { bold: true, size: 18 }), widths[i], BAND)
    ),
  });
}

function sectionHeading(text) {
  return new Paragraph({
    spacing: { before: 320, after: 140 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: INK } },
    children: [
      new TextRun({ text, bold: true, size: 26, color: INK, font: "Calibri" }),
    ],
  });
}

function groupLabel(text) {
  return new Paragraph({
    spacing: { before: 180, after: 60 },
    children: [
      new TextRun({ text: text.toUpperCase(), bold: true, size: 16, color: MUTED, font: "Calibri" }),
    ],
  });
}

// ---------- block A ----------
function blockARow(label, field, widths) {
  return new TableRow({
    children: [
      cell(
        [
          cellPara(label, null, { bold: true, size: 18 }),
          cellPara(val(field) || "— not found —", src(field), {
            color: val(field) ? INK : MUTED,
          }),
        ],
        widths[0]
      ),
      cell(cellPara(""), widths[1]),
      cell(cellPara(""), widths[2]),
    ],
  });
}

function blockA(r) {
  const out = [
    sectionHeading("Block A — Confirm this"),
    p(
      "Everything below we found publicly. Tick the middle column if it's right, or write the correction in the last column. Bulk-approving this block is fine.",
      { italic: true, color: MUTED, size: 18, after: 160 }
    ),
  ];

  const groups = [
    ["Identity", [
      ["Business name", r.identity?.business_name],
      ["Address", r.identity?.address],
      ["Address type", r.identity?.address_type],
      ["Mailing address", r.identity?.mailing_address],
    ]],
    ["Contact", [
      ["Main phone", r.contact?.primary_phone],
      ["After-hours phone", r.contact?.after_hours_phone],
      ["Email", r.contact?.email],
      ["Contact form goes to", r.contact?.form_destination],
      ["Booking link", r.contact?.booking_link],
    ]],
    ["Hours", [
      ["Regular hours", r.hours?.regular],
      ["Seasonal changes", r.hours?.seasonal],
    ]],
    ["Service area", [
      ["Furthest north", r.service_area?.furthest_north],
      ["Furthest south", r.service_area?.furthest_south],
      ["Furthest east", r.service_area?.furthest_east],
      ["Furthest west", r.service_area?.furthest_west],
      ["Cities claimed on site", r.service_area?.claimed_cities],
      ["Anywhere you won't go", r.service_area?.exclusions],
      ["Travel fee beyond that", r.service_area?.travel_fee],
    ]],
    ["Online", [
      ["Website platform", r.online?.platform],
      ["Google Business Profile", r.online?.gbp_url],
    ]],
  ];

  for (const [name, rows] of groups) {
    const present = rows.filter(([, f]) => f !== undefined);
    if (!present.length) continue;
    out.push(groupLabel(name));
    out.push(
      table(
        [
          headerRow(["What we have", "Correct?", "Fix it here"], COLS_A),
          ...present.map(([label, f]) => blockARow(label, f, COLS_A)),
        ],
        COLS_A
      )
    );
  }

  // services checklist
  const svc = r.services?.found || [];
  if (svc.length) {
    out.push(groupLabel("Services"));
    out.push(
      p(
        "Mark each: keep / dropped. Then circle up to three you want MORE of, and X any you'd rather stop getting calls for.",
        { italic: true, color: MUTED, size: 18 }
      )
    );
    const w = [4200, 1100, 1100, 1100, 1860];
    out.push(
      table(
        [
          headerRow(["Service", "Keep", "Dropped", "Want more", "Notes"], w),
          ...svc.map((s) =>
            new TableRow({
              children: [
                cell(cellPara(s.name || "", s.source), w[0]),
                cell(cellPara(""), w[1]),
                cell(cellPara(""), w[2]),
                cell(cellPara(""), w[3]),
                cell(cellPara(""), w[4]),
              ],
            })
          ),
          new TableRow({
            children: [
              cell(cellPara("Anything missing? Add here →", null, { bold: true }), w[0]),
              cell(cellPara(""), w[1]),
              cell(cellPara(""), w[2]),
              cell(cellPara(""), w[3]),
              cell(cellPara(""), w[4]),
            ],
          }),
        ],
        w
      )
    );
  }

  const dupes = r.online?.duplicate_listings || [];
  if (dupes.length) {
    out.push(groupLabel("Heads up"));
    out.push(
      p(
        `We found ${dupes.length} other Google listing(s) that may be yours: ${dupes
          .map((d) => (typeof d === "string" ? d : d.value || d.url || ""))
          .join(" · ")}. Do you recognise these?`,
        { size: 18 }
      )
    );
  }

  return out;
}

// ---------- block B ----------
function blockB(r) {
  const claims = (r.claims || []).filter(
    (c) => c && (c.quoted || (c.conflict && c.conflict.length))
  );
  const out = [
    sectionHeading("Block B — Please verify these claims"),
    p(
      "These are things your website or listings already say publicly. We won't republish any of them without your sign-off. Please answer each one individually.",
      { italic: true, color: MUTED, size: 18, after: 160 }
    ),
  ];

  if (!claims.length) {
    out.push(p("No public claims found to verify.", { color: MUTED, italic: true }));
    return out;
  }

  const rows = [headerRow(["The claim", "True? / Correction"], COLS_B)];

  for (const c of claims) {
    if (c.conflict && c.conflict.length) {
      const lines = [
        cellPara(prettyField(c.field), null, { bold: true, size: 18 }),
        cellPara("Sources disagree — which is right?", null, { italic: true, color: MUTED, size: 16 }),
        ...c.conflict.map((v) =>
          cellPara(`• ${v.value}`, v.source, {})
        ),
      ];
      rows.push(
        new TableRow({
          children: [cell(lines, COLS_B[0], FLAG), cell(cellPara(""), COLS_B[1], FLAG)],
        })
      );
    } else {
      rows.push(
        new TableRow({
          children: [
            cell(
              [
                cellPara(prettyField(c.field), null, { bold: true, size: 18 }),
                cellPara(`"${c.quoted}"`, c.source, {}),
              ],
              COLS_B[0]
            ),
            cell(cellPara(""), COLS_B[1]),
          ],
        })
      );
    }
  }

  out.push(table(rows, COLS_B));
  return out;
}

function prettyField(f) {
  if (!f) return "";
  return String(f)
    .replace(/_/g, " ")
    .replace(/^\w/, (c) => c.toUpperCase());
}

// ---------- block C ----------
function blockC(r) {
  const n = r.needed || {};
  const out = [
    sectionHeading("Block C — We need this from you"),
    p(
      "We couldn't find these anywhere, and we can't guess them. This is the part that actually matters — a sentence is plenty for the written ones.",
      { italic: true, color: MUTED, size: 18, after: 160 }
    ),
  ];

  if ((n.documents || []).length) {
    out.push(groupLabel("Just forward these — no typing needed"));
    for (const d of n.documents) out.push(p(`☐   ${d}`, { size: 20 }));
  }

  if ((n.facts || []).length) {
    const w = [4200, 5160];
    out.push(groupLabel("Facts"));
    out.push(
      table(
        (n.facts || []).map((f) =>
          new TableRow({
            children: [
              cell(cellPara(typeof f === "string" ? f : f.label, null, { bold: true, size: 18 }), w[0]),
              cell(cellPara(""), w[1]),
            ],
          })
        ),
        w
      )
    );
  }

  if ((n.positioning || []).length) {
    out.push(groupLabel("Three questions — one sentence each is fine"));
    for (const q of n.positioning) {
      out.push(p(q, { bold: true, size: 20, before: 120, after: 40 }));
      out.push(
        new Paragraph({
          spacing: { after: 200 },
          border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: "C8C8C8" } },
          children: [new TextRun({ text: " ", size: 20 })],
        })
      );
    }
  }

  out.push(groupLabel("Your team"));
  out.push(
    p("Names, job titles, and a photo for anyone who should appear on the site. That's all for now — we'll get the rest from you on a call.", { size: 18, color: MUTED, italic: true })
  );
  const w = [3600, 3600, 2160];
  out.push(
    table(
      [
        headerRow(["Name", "Role", "Photo?"], w),
        ...Array.from({ length: Math.max(3, (n.people || []).length) }, (_, i) => {
          const person = (n.people || [])[i] || {};
          return new TableRow({
            children: [
              cell(cellPara(person.name || ""), w[0]),
              cell(cellPara(person.role || ""), w[1]),
              cell(cellPara(""), w[2]),
            ],
          });
        }),
      ],
      w
    )
  );

  return out;
}

// ---------- access ----------
function accessBlock(r) {
  const items = r.access || [];
  const out = [
    sectionHeading("Access"),
    p(
      "This is the part that holds everything else up. \"Don't know\" is a perfectly good answer — if someone else set it up originally, just tell us who.",
      { italic: true, color: MUTED, size: 18, after: 160 }
    ),
    table(
      [
        headerRow(["What", "Who has it", "Sent? / Don't know"], COLS_ACCESS),
        ...items.map((a) =>
          new TableRow({
            children: [
              cell(cellPara(a.item || "", null, { bold: true, size: 18 }), COLS_ACCESS[0]),
              cell(cellPara(a.owner || ""), COLS_ACCESS[1]),
              cell(cellPara(""), COLS_ACCESS[2]),
            ],
          })
        ),
      ],
      COLS_ACCESS
    ),
  ];
  return out;
}

// ---------- document ----------
function build(r) {
  const m = r.meta || {};
  const head = [
    new Paragraph({
      spacing: { after: 40 },
      children: [
        new TextRun({
          text: m.business_name || "Client",
          bold: true,
          size: 36,
          font: "Calibri",
        }),
      ],
    }),
    p(
      `Prepared ${m.prepared || ""}${m.return_by ? `  ·  Please return by ${m.return_by}` : ""}`,
      { color: MUTED, size: 18, after: 160 }
    ),
    p(
      "We've already filled in everything we could find about your business publicly. You don't need to write much — just fix what's wrong and fill the blanks we couldn't find. Should take about ten minutes.",
      { size: 20, after: 60 }
    ),
    p(
      m.return_by
        ? `If we don't hear back by ${m.return_by}, we'll build with what's on here now.`
        : "If we don't hear back, we'll build with what's on here now.",
      { size: 20, bold: true, after: 120 }
    ),
  ];

  const foot = [
    new Paragraph({
      spacing: { before: 400 },
      border: { top: { style: BorderStyle.SINGLE, size: 6, color: "C8C8C8" } },
      children: [new TextRun({ text: " ", size: 16 })],
    }),
    p(
      `Would rather do this over the phone? Call ${m.manager || "us"} and we'll fill it in while we talk — takes about five minutes.`,
      { size: 20, bold: true }
    ),
  ];

  return new Document({
    sections: [
      {
        properties: { page: { size: PAGE, margin: { top: 1080, bottom: 1080, left: 1440, right: 1440 } } },
        children: [
          ...head,
          ...blockA(r),
          ...blockB(r),
          ...blockC(r),
          ...accessBlock(r),
          ...foot,
        ],
      },
    ],
  });
}

// ---------- main ----------
async function main() {
  const inPath = process.argv[2];
  if (!inPath) {
    console.error("usage: node render_proof_sheet.js <record.yaml> [output.docx]");
    process.exit(1);
  }
  const r = loadRecord(inPath);
  const out =
    process.argv[3] ||
    `${(r.meta && r.meta.slug) || path.basename(inPath).replace(/\.\w+$/, "")}-proof-sheet.docx`;
  const buf = await Packer.toBuffer(build(r));
  fs.writeFileSync(out, buf);
  console.log(`wrote ${out}`);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
