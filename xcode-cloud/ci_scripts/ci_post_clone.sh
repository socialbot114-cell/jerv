#!/bin/sh
set -eu

# Xcode Cloud runs this script after checkout. The generated project is kept
# reproducible by deriving it from the checked-in XcodeGen specification.
cd "$CI_PRIMARY_REPOSITORY_PATH"
if command -v brew >/dev/null 2>&1; then
  brew install xcodegen || true
fi
project_dir="."
if [ -d iosApp ]; then
  project_dir=iosApp
fi
xcodegen generate --spec "$project_dir/project.yml"
python3 tools/jerv_cli.py release-check app.yml
