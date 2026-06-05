Data files used by the project

This folder contains small JSON assets that the application uses as
fallbacks, defaults, and lightweight reference tables. They are read-only
at runtime and are intended to be human-editable.

Files:

- `city_costs.json` : Per-city cost multipliers and example pricing used by
  the budget estimator when live pricing isn't available.
- `city_metadata.json` : Human-friendly city names, timezones, and
  optional local-currency hints used when formatting results.
- `crowd_rules.json` : Simple heuristics and thresholds used by the crowd
  estimation service to produce crowd-level suggestions.
- `holidays.json` : A compact list of public holidays used to warn about
  peak travel dates and closures.

Notes:
- These files are plain JSON; do not add comments inside them. Instead,
  edit this README to explain changes or to document data sources.
- Keep files UTF-8 encoded. Small edits are safe in development; in
  production, manage them via source control or a configuration service.
