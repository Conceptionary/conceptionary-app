/* Conceptionary template list - THE ONE PLACE to add, rename or remove a template.
   Used by templates.html (the launcher) and view.html (the Home / Previous / Next bar).
   Each entry: id, label, rom (file name without .html, or null), log (same, or null).
   Files live in templates/phonographic/ (ROM-...) and templates/logographic/ (LOG-...);
   worked examples (names ending -ID-EN or -JA-EN) live in examples/id-en/ and examples/ja-en/.
   A link whose file does not exist in the repo is hidden automatically on the live site.
   (c) 2026 Alan William Preston */
window.CONCEPTIONARY_TEMPLATE_FAMILIES = [
  { name: 'Single Line', items: [
    { id: 'VL',      label: 'Vertical Line (VL)',         rom: 'ROM-VL-Generic',      log: 'LOG-VL-Generic' },
    { id: 'HL-5TB',  label: 'Horizontal Line, 5 (HL-5TB)',  rom: 'ROM-HL-5TB-Generic',  log: 'LOG-HL-5TB-Generic' },
    { id: 'HL-10TB', label: 'Horizontal Line, 10 (HL-10TB)', rom: 'ROM-HL-10TB-Generic', log: 'LOG-HL-10TB-Generic' },
    { id: 'DU',      label: 'Diagonal Up (DU)',           rom: 'ROM-DU-Generic',      log: 'LOG-DU-Generic' },
    { id: 'DD',      label: 'Diagonal Down (DD)',         rom: 'ROM-DD-Generic',      log: 'LOG-DD-Generic' }
  ]},
  { name: 'Bidirectional', items: [
    { id: 'HL-BI', label: 'Horizontal Bidirectional (HL-BI)', rom: 'ROM-HL-BI-Generic', log: 'LOG-HL-BI-Generic' },
    { id: 'CV-BI', label: 'Curve Bidirectional (CV-BI)',      rom: 'ROM-CV-BI-Generic', log: 'LOG-CV-BI-Generic' }
  ]},
  { name: 'Instant Change', items: [
    { id: 'IT5L',       label: 'IT5L',       rom: 'ROM-IT5L-Generic',       log: 'LOG-IT5L-7TB-Generic' },
    { id: 'IT5L-11TB',  label: 'IT5L-11TB',  rom: 'ROM-IT5L-11TB-Generic',  log: 'LOG-IT5L-11TB-Generic' },
    { id: 'IT5LI',      label: 'IT5LI (inverted)',      rom: 'ROM-IT5LI-Generic',      log: 'LOG-IT5LI-5TB-Generic' },
    { id: 'IT5LI-11TB', label: 'IT5LI-11TB (inverted)', rom: 'ROM-IT5LI-11TB-Generic', log: 'LOG-IT5LI-11TB-Generic' },
    { id: 'IP3LP',      label: 'IP3LP (positive)',      rom: 'ROM-IP3LP-Generic',      log: 'LOG-IP3LP-Generic' },
    { id: 'IP3LN',      label: 'IP3LN (negative)',      rom: 'ROM-IP3LN-Generic',      log: 'LOG-IP3LN-Generic' }
  ]},
  { name: 'Gradual Change', items: [
    { id: 'GT5L-7TB',   label: 'GT5L-7TB',   rom: 'ROM-GT5L-7TB-Generic',   log: 'LOG-GT5L-7TB-Generic' },
    { id: 'GT5L-11TB',  label: 'GT5L-11TB',  rom: 'ROM-GT5L-11TB-Generic',  log: 'LOG-GT5L-11TB-Generic' },
    { id: 'GT5LI',      label: 'GT5LI (inverted)', rom: 'ROM-GT5LI-Generic', log: 'LOG-GT5LI-11TB-Generic' },
    { id: 'GP3LP-7TB',  label: 'GP3LP-7TB (positive)', rom: 'ROM-GP3LP-7TB-Generic', log: 'LOG-GP3LP-7TB-Generic' },
    { id: 'GP3LN-7TB',  label: 'GP3LN-7TB (negative)', rom: 'ROM-GP3LN-7TB-Generic', log: 'LOG-GP3LN-7TB-Generic' }
  ]},
  { name: 'Bell Curve', items: [
    { id: 'GTCV',        label: 'GTCV',                 rom: 'ROM-GTCV-Generic',        log: 'LOG-GTCV-Generic' },
    { id: 'GTCVI-Wide',  label: 'GTCVI-Wide (inverted)',    rom: 'ROM-GTCVI-Wide-Generic',    log: 'LOG-GTCVI-Wide-Generic' },
    { id: 'GTCVI-Shallow', label: 'GTCVI-Shallow (inverted)', rom: 'ROM-GTCVI-Shallow-Generic', log: 'LOG-GTCVI-Shallow-Generic' },
    { id: 'GPCVP',       label: 'GPCVP (positive)',     rom: 'ROM-GPCVP-Generic',       log: 'LOG-GPCVP-Generic' },
    { id: 'GPCVN',       label: 'GPCVN (negative)',     rom: 'ROM-GPCVN-Generic',       log: 'LOG-GPCVN-Generic' }
  ]},
  { name: 'Hybrid Temporary', items: [
    { id: 'HTCVS',  label: 'HTCVS: curve, then sudden drop',            rom: 'ROM-HTCVS-Generic',  log: 'LOG-HTCVS-Generic' },
    { id: 'HTSCV',  label: 'HTSCV: sudden rise, then curve',            rom: 'ROM-HTSCV-Generic',  log: 'LOG-HTSCV-Generic' },
    { id: 'HTCVSI', label: 'HTCVSI: curve down, sudden return',         rom: 'ROM-HTCVSI-Generic', log: 'LOG-HTCVSI-Generic' },
    { id: 'HTSCVI', label: 'HTSCVI: sudden drop, curve back up',        rom: 'ROM-HTSCVI-Generic', log: 'LOG-HTSCVI-Generic' }
  ]},
  { name: 'Circular', items: [
    { id: 'CR-CAL-North', label: 'Calendar, Northern Hemisphere (CR-CAL-North)', rom: 'ROM-CR-CAL-North-Generic', log: 'LOG-CR-CAL-North-Generic' },
    { id: 'CR-CAL-South', label: 'Calendar, Southern Hemisphere (CR-CAL-South)', rom: 'ROM-CR-CAL-South-Generic', log: 'LOG-CR-CAL-South-Generic' },
    { id: 'CR-CLK',  label: 'CR-CLK',  rom: 'ROM-CR-CLK-Generic',  log: 'LOG-CR-CLK-Generic' },
    { id: 'CR-TTT',  label: 'CR-TTT',  rom: 'ROM-CR-TTT-Generic',  log: 'LOG-CR-TTT-Generic' },
    { id: 'CR-TDL',  label: 'CR-TDL',  rom: 'ROM-CR-TDL-Generic',  log: 'LOG-CR-TDL-Generic' },
    { id: 'CR-DAY',  label: 'CR-DAY',  rom: 'ROM-CR-DAY-Generic',  log: 'LOG-CR-DAY-Generic' },
    { id: 'CR-DOW',  label: 'CR-DOW',  rom: 'ROM-CR-DOW-Generic',  log: 'LOG-CR-DOW-Generic' },
    { id: 'CR-MOY',  label: 'CR-MOY',  rom: 'ROM-CR-MOY-Generic',  log: 'LOG-CR-MOY-Generic' },
    { id: 'CR-SEA-WET',    label: 'CR-SEA-WET',    rom: 'ROM-CR-SEA-WET-Generic',    log: 'LOG-CR-SEA-WET-Generic' },
    { id: 'CR-SEA-TEMP-S', label: 'CR-SEA-TEMP-S', rom: 'ROM-CR-SEA-TEMP-S-Generic', log: 'LOG-CR-SEA-TEMP-S-Generic' },
    { id: 'CR-SEA-TEMP-N', label: 'CR-SEA-TEMP-N', rom: 'ROM-CR-SEA-TEMP-N-Generic', log: 'LOG-CR-SEA-TEMP-N-Generic' },
    { id: 'CR-TML',  label: 'CR-TML',  rom: 'ROM-CR-TML-Generic',  log: 'LOG-CR-TML-Generic' },
    { id: 'CR-LUN',  label: 'CR-LUN',  rom: 'ROM-CR-LUN-Generic',  log: 'LOG-CR-LUN-Generic' },
    { id: 'CR-MEN',  label: 'CR-MEN',  rom: 'ROM-CR-MEN-Generic',  log: 'LOG-CR-MEN-Generic' },
    { id: 'CR-CMP',  label: 'CR-CMP',  rom: 'ROM-CR-CMP-Generic',  log: 'LOG-CR-CMP-Generic' },
    { id: 'CR-SW',   label: 'CR-SW',   rom: 'ROM-CR-SW-Generic',   log: 'LOG-CR-SW-Generic' }
  ]},
  { name: 'Tense Timeline', items: [
    { id: 'TRG', label: 'Tense timeline: past, present, future (TRG)', rom: 'ROM-TRG-Generic', log: null }
  ]},
  /* Worked examples (a real language pair, with recorded audio). Files live in examples/id-en/ and examples/ja-en/.
     'intro' puts the big "Example templates" heading above the first group; 'anchor' is the id the top link jumps to. */
  { name: 'Indonesian for English speakers', intro: 'Example templates', anchor: 'examples', items: [
    { id: 'EX-ID-TDL', label: 'Daily Tidal Cycle (CR-TDL)',  rom: 'ROM-CR-TDL-ID-EN', log: null },
    { id: 'EX-ID-MOY', label: 'Months of the Year (CR-MOY)', rom: 'ROM-CR-MOY-ID-EN', log: null },
    { id: 'EX-ID-DOW', label: 'Days of the Week (CR-DOW)',   rom: 'ROM-CR-DOW-ID-EN', log: null }
  ]},
  { name: 'Japanese for English speakers', items: [
    { id: 'EX-JA-TDL', label: 'Daily Tidal Cycle (CR-TDL)',  rom: null, log: 'LOG-CR-TDL-JA-EN' },
    { id: 'EX-JA-MOY', label: 'Months of the Year (CR-MOY)', rom: null, log: 'LOG-CR-MOY-JA-EN' }
  ]}
];

/* Helpers shared by both pages */
window.CONCEPTIONARY_NAV = (function () {
  var fams = window.CONCEPTIONARY_TEMPLATE_FAMILIES;
  var flat = [];
  fams.forEach(function (f) { f.items.forEach(function (t) { t.family = f.name; flat.push(t); }); });
  function folder(file) {
    if (/-ID-EN$/.test(file)) return 'examples/id-en/';   /* worked examples: Indonesian for English speakers */
    if (/-JA-EN$/.test(file)) return 'examples/ja-en/';   /* worked examples: Japanese for English speakers */
    return file.indexOf('ROM-') === 0 ? 'templates/phonographic/' : 'templates/logographic/';
  }
  function find(file) {
    for (var i = 0; i < flat.length; i++) {
      if (flat[i].rom === file) return { t: flat[i], kind: 'rom', i: i };
      if (flat[i].log === file) return { t: flat[i], kind: 'log', i: i };
    }
    return null;
  }
  return { families: fams, flat: flat, folder: folder, find: find };
})();