# Conceptionary
2026-08-21
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

## Running it

`Conceptionary_App.html` loads local project data via a folder-picker
(Chrome's File System Access API, with a fallback for Firefox/Safari) —
click **Load** inside the app and select your local clone of this
repository. It reads `registry/`, `concept_cards/`, and `templates/`
directly from whatever folder is selected.

## Structure

```
Conceptionary_App.html      the application
registry/                   the concept registry and location index data
concept_cards/               vocabulary content, one JSON file per concept
templates/
  phonographic/               templates for alphabetic/romanized target languages
  logographic/                templates for Japanese, Chinese, Korean, Arabic, Thai
```

## License

© 2026 Alan William Preston
 
