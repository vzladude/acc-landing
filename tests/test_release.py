"""Check deployable assets, indexing metadata and deployment target safeguards."""
import importlib.util
import json
import os
import re
import subprocess
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('builder', ROOT / 'scripts/build_site.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.destination = Path(self.temp.name) / 'release'
        self.override = patch.object(builder, 'DESTINATION', self.destination)
        self.override.start()

    def tearDown(self):
        self.override.stop()
        self.temp.cleanup()

    def test_release_includes_inline_svg_and_css_images_with_unchanged_image_bytes(self):
        builder.build()
        page = (self.destination / 'index.html').read_text()
        self.assertRegex(page, r'img/acc-logo\.[a-f0-9]{16}\.png')
        for original in (ROOT / 'img').rglob('*'):
            if original.is_file() and original.suffix.lower() in builder.EXTENSIONS:
                relative = original.relative_to(ROOT).as_posix()
                renamed = builder.fingerprint(relative, original.read_bytes())
                self.assertEqual((self.destination / renamed).read_bytes(), original.read_bytes())
        css = next((self.destination / 'css').glob('styles.*.css')).read_text()
        for raw in re.findall(r'url\("([^"]+)"\)', css):
            self.assertTrue((self.destination / 'css' / raw).is_file(), raw)
        self.assertFalse(list(self.destination.rglob('*.md')))
        self.assertFalse((self.destination / 'deploy').exists())
        self.assertFalse((self.destination / 'release-manifest.json').exists())

    def test_indexing_and_social_metadata_share_official_host(self):
        builder.build()
        page = (self.destination / 'index.html').read_text()
        self.assertNotIn('github.io', page)
        self.assertNotIn('noindex', page)
        self.assertIn(f'rel="canonical" href="{builder.PRODUCTION_URL}"', page)
        urls = ET.parse(self.destination / 'sitemap.xml').findall('.//{*}loc')
        self.assertEqual([url.text for url in urls], [builder.PRODUCTION_URL])
        self.assertIn(builder.PRODUCTION_URL + 'sitemap.xml', (self.destination / 'robots.txt').read_text())
        for image in re.findall(r'(?:og:image|twitter:image)" content="([^"]+)"', page):
            self.assertTrue((self.destination / image.removeprefix(builder.PRODUCTION_URL)).is_file())

    def test_rebuilding_produces_identical_manifest(self):
        builder.build()
        manifest = (self.destination.parent / 'release-manifest.json').read_bytes()
        builder.build()
        self.assertEqual(manifest, (self.destination.parent / 'release-manifest.json').read_bytes())

    def test_rejects_preview_metadata_or_missing_images(self):
        original = Path.read_text
        for replacement in ['<meta name="robots" content="noindex">', '<img src="./img/missing.png" alt="">']:
            def read(path, *args, **kwargs):
                content = original(path, *args, **kwargs)
                return content.replace('</head>', replacement + '</head>') if path == ROOT / 'index.html' else content
            with self.subTest(replacement=replacement), patch.object(Path, 'read_text', read), self.assertRaises(ValueError):
                builder.build()


class DeployTests(unittest.TestCase):
    def test_rejects_missing_or_incorrect_targets_before_any_write(self):
        with tempfile.TemporaryDirectory() as temp:
            fake = Path(temp) / 'aws'
            fake.write_text('#!/bin/sh\ncase "$*" in\n*get-caller-identity*) echo "${TEST_ACCOUNT:-767397867309}";;\n*get-distribution-config*) echo "wrong-bucket.s3.us-east-1.amazonaws.com";;\n*) echo UNEXPECTED_WRITE >&2; exit 77;;\nesac\n')
            fake.chmod(0o755)
            env = {k: v for k, v in os.environ.items() if k not in ['S3_BUCKET', 'CLOUDFRONT_DISTRIBUTION_ID', 'SITE_URL', 'ALLOW_INDEXING']}
            env['PATH'] = temp + os.pathsep + env['PATH']
            cases = [({}, 'Set S3_BUCKET'),
                     ({'S3_BUCKET': 'acc-landing-production-767397867309'}, 'Set S3_BUCKET'),
                     ({'S3_BUCKET': 'wrong', 'CLOUDFRONT_DISTRIBUTION_ID': 'TEST'}, 'account or bucket'),
                     ({'S3_BUCKET': 'acc-landing-production-767397867309', 'CLOUDFRONT_DISTRIBUTION_ID': 'TEST', 'TEST_ACCOUNT': 'wrong'}, 'account or bucket'),
                     ({'S3_BUCKET': 'acc-landing-production-767397867309', 'CLOUDFRONT_DISTRIBUTION_ID': 'TEST'}, 'origin does not match')]
            for values, message in cases:
                with self.subTest(values=values):
                    result = subprocess.run(['bash', str(ROOT / 'deploy.sh'), '--dry-run'], env=env | values, capture_output=True, text=True)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(message, result.stderr)
                    self.assertNotIn('UNEXPECTED_WRITE', result.stderr)


if __name__ == '__main__':
    unittest.main()
