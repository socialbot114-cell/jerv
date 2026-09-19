# JERV App Factory

JERV is the reusable app-delivery skill for the Brasilia app portfolio.
It generates project scaffolding, validates release contracts, audits source
trees, and prepares deterministic CI gates for iOS apps.

## Non-negotiable rules

- Never store `.p8`, `.cer`, `.key`, `.mobileprovision`, `.jks`, `.keystore`,
  `keystore.properties`, API keys, or tokens in JERV.
- Deterministic checks block releases. Jev/TypeSafe prioritization is optional
  and must never be the only release gate.
- Every catalog record must retain its source and collection date.
- A product must not claim reservations, appointments, ratings, or live data
  unless that capability is implemented and tested.

## Local usage

```sh
python3 jerv_cli.py validate path/to/app.yml
python3 jerv_cli.py audit path/to/app.yml
python3 jerv_cli.py release-check path/to/app.yml
python3 jerv_cli.py init path/to/new-app --manifest path/to/app.yml
```

The CLI requires Python 3.10+ and PyYAML. `audit` is local and deterministic;
the existing `worker/` scripts remain optional Jev prioritization workers.

## App contract

Each product owns an `app.yml` based on `schemas/app.yml`. The contract drives
XcodeGen, catalog validation, CI artifact names, and bundle verification.

## Reuse model

- `templates/` contains product-neutral iOS scaffolding.
- `workflows/` contains reusable GitHub Actions workflows.
- `xcode-cloud/` contains scripts copied into each app repository because
  Xcode Cloud executes scripts from the checked-out repository.
- `reports/` remains the historical and sanitized audit record.
