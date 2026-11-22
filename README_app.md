# Conceptionary
2026-11-22
An interactive vocabulary-learning system built on a simple idea: a word's
position on a visual template encodes its meaning. Instead of an
alphabetical list, a concept like "quality" or "freshness" is laid out as
a shape — a curve, a line, a spectrum — and vocabulary sits at the point
on that shape where it belongs. Learners explore relationships between
words spatially, not by looking them up.

Vocabulary is also organised by where it occurs in real life — a
five-tier spatial index (Home → Kitchen → Fridge → Top shelf, for
example) lets a learner browse a map of everyday places and find the
language that belongs there, the way people actually encounter words in
context rather than in a dictionary.

Originally conceived in 1992; in active development since 2024.

## Status

Early stage, under active construction. The template system (70+ generic
templates across both phonographic and logographic language tracks) and
the spatial location index (Personal/Home zone complete, Educational and
Work zones in progress) are both substantially built. One concept —
*Freshness of Dairy Products*, English → Bahasa Indonesia — is wired
end-to-end as a working proof of the full pipeline: navigate the map,
land on a real template, see real vocabulary. Most locations are not yet
populated with content.

**Circular ("CR") family.** The circular templates (months of the year,
days of the week, lunar and tidal cycles, seasons, rice growing, steering
wheel, compass, parts of the day, clock, calendar and telling the time)
now share one phone kit: pinch-zoom, a Full Screen zoom, a Quiz that sits
at the top of a phone screen, Reset, a Learned counter, and 44 px touch
targets. Each exists as a phonographic (ROM) and a logographic (LOG)
version.

**Worked models.** Ready-made language-pair examples (target language →
source language) are provided for several of these templates, in
Indonesian → English and Japanese → English, plus German and Indonesian
examples for the seasons templates. Their vocabulary was drafted with
Claude's help and is still being reviewed.

## Running it

`index.html` is the application. It loads local project data via a folder-picker
(Chrome's File System Access API, with a fallback for Firefox/Safari) —
click **Load** inside the app and select your local clone of this
repository. It reads `registry/`, `concept_cards/`, and `templates/`
directly from whatever folder is selected.

**Template list (phone, tablet and desktop).** The published site also
has a template list page (`templates.html`) that opens any template or
worked example in a viewer, with Home / Prev / Next and Full Screen. It
can be installed as an offline app: open the site once online, then press
**Update** after each new push so the phone downloads the new files.

## Structure

```
index.html                  the application
templates.html, view.html   template list page and viewer
registry/                   the concept registry and location index data
concept_cards/               vocabulary content, one JSON file per concept
templates/
  phonographic/               templates for alphabetic/romanized target languages
  logographic/                templates for Japanese, Chinese, Korean, Arabic, Thai
examples/
  id-en/, ja-en/, en-de/      worked language-pair models
conceptionary-templates.js  list of templates and examples shown on the list page
conceptionary-update.js     the Update button
kit.js, kit.css, kit_patch.py   shared phone kit and the tool that applies it
sw.js, manifest.webmanifest, icons/   offline installation
Conceptionary_diacritic_spelling_conventions.html   spelling conventions for diacritic input
```

## License

© 2026 Alan William Preston