import json
import tempfile
import unittest
from pathlib import Path

import jerv_cli


class JervCliTests(unittest.TestCase):
    def write_app(self, root: Path, status: str = "verified") -> Path:
        (root / "Resources" / "Catalog").mkdir(parents=True)
        (root / "Resources" / "PrivacyInfo.xcprivacy").write_text("{}", encoding="utf-8")
        (root / "Resources" / "Catalog" / "catalog.json").write_text(
            json.dumps([{"id": "one", "name": "One", "source": "test", "last_verified": "2026-01-01", "data_status": status}]),
            encoding="utf-8",
        )
        manifest = root / "app.yml"
        manifest.write_text(
            "\n".join([
                "name: Test App",
                "product_name: TestApp",
                "bundle_id: br.com.test.app",
                "sku: test-app",
                'app_store_id: "123"',
                "platform: ios",
                "template: ios-swiftui-directory",
                "catalog:",
                "  path: Resources/Catalog/catalog.json",
                "  required_fields: [id, name, source, last_verified]",
                "privacy_manifest: Resources/PrivacyInfo.xcprivacy",
                "release:",
                "  artifact_name: test-ipa",
                "  scheme: TestApp",
            ]) + "\n",
            encoding="utf-8",
        )
        return manifest

    def test_verified_catalog_passes_release_check(self):
        with tempfile.TemporaryDirectory() as directory:
            manifest = self.write_app(Path(directory))
            self.assertEqual(jerv_cli.run_validation(manifest, release=True), 0)

    def test_unverified_catalog_blocks_release(self):
        with tempfile.TemporaryDirectory() as directory:
            manifest = self.write_app(Path(directory), status="pending-rights-review")
            self.assertEqual(jerv_cli.run_validation(manifest, release=True), 1)

    def test_uppercase_bundle_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            manifest = self.write_app(Path(directory))
            text = manifest.read_text(encoding="utf-8").replace("br.com.test.app", "br.com.Test.app")
            manifest.write_text(text, encoding="utf-8")
            self.assertEqual(jerv_cli.run_validation(manifest), 1)


if __name__ == "__main__":
    unittest.main()
