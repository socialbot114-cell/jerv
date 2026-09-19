# Reusable Pipeline

Each app repository contains `app.yml`, `project.yml`, and a catalog.
The app repository may copy the Xcode Cloud script from `xcode-cloud/ci_scripts`.
GitHub Actions should call the reusable workflows from this repository at a
fixed tag or commit, never `main`.

## Required app repository files

```text
app.yml
tools/jerv_cli.py
project.yml
Info.plist
Resources/PrivacyInfo.xcprivacy
Resources/Catalog/catalog.json
.github/workflows/validate.yml
```

## Release ownership

GitHub Actions performs validation and produces a signed artifact only when
explicitly requested. Xcode Cloud is the recommended owner of the official
TestFlight archive. Do not enable automatic TestFlight upload in both systems.

## Secrets

All signing material is configured in the CI provider. JERV scans the checked
out tree and blocks secret-like files before release.
