import os
from pathlib import Path
import subprocess
import tarfile
import tempfile
import unittest

import yaml

WORKFLOW = '.github/workflows/generate-package.yml'


class PackageContentsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).resolve().parents[1]
        workflow = yaml.safe_load((root / WORKFLOW).read_text())
        commands = next(step['run'] for step in workflow['jobs']['create-release']['steps'] if step.get('name') == 'Create the tar.gz package')
        cls.plugin_name = 'examplePlugin'
        cls.runtime_files = [
            'version.xml', 'README.md', 'LICENSE', 'index.php',
            'classes/Plugin.php', 'templates/settings.tpl', 'locale/en/locale.po',
            'styles/plugin.css', 'public/build/build.iife.js',
            'vendor/runtime/library.php',
        ]
        cls.excluded = [
            'AGENTS.md', 'CLAUDE.md', 'tests', 'cypress', 'node_modules',
            '.git', '.gitignore', '.gitattributes', '.gitlab-ci.yml',
            '.github', '.codex', '.agents', '.vscode', '.githooks',
        ]
        directories = {'tests', 'cypress', 'node_modules', '.git', '.github', '.codex', '.agents', '.vscode', '.githooks'}
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            checkout = base / 'checkout'
            checkout.mkdir()
            staging = base / 'staging'
            staging.mkdir()
            for filename in cls.runtime_files + [name + '/fixture' if name in directories else name for name in cls.excluded]:
                path = checkout / filename
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('fixture')
            script = base / 'build.sh'
            script.write_text(commands)
            result = subprocess.run(
                ['bash', '-eo', 'pipefail', str(script)], cwd=checkout,
                env={**os.environ, 'PLUGIN_NAME': cls.plugin_name, 'CI_PROJECT_DIR': str(checkout), 'TMPDIR': str(staging)},
                capture_output=True, text=True,
            )
            if result.returncode:
                raise RuntimeError(result.stderr + result.stdout)
            with tarfile.open(checkout / (cls.plugin_name + '.tar.gz')) as package:
                cls.members = {member.name.rstrip('/') for member in package.getmembers()}

    def test_excludes_development_files(self):
        for filename in self.excluded:
            with self.subTest(filename=filename):
                path = self.plugin_name + '/' + filename
                self.assertFalse(any(name == path or name.startswith(path + '/') for name in self.members), filename)

    def test_preserves_runtime_files_under_one_plugin_root(self):
        self.assertEqual({self.plugin_name}, {name.split('/')[0] for name in self.members})
        for filename in self.runtime_files:
            with self.subTest(filename=filename):
                self.assertIn(self.plugin_name + '/' + filename, self.members)


if __name__ == '__main__':
    unittest.main()
