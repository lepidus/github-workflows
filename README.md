# github-workflows

**English** | [Português Brasileiro](docs/README-pt_BR.md) | [Español](docs/README-es.md)

Reusable GitHub Actions workflows for Lepidus plugins.

## Available workflows

### `generate-package.yml`

Validates `version.xml`, generates a `.tar.gz` package, and publishes a complete English release when a tag is pushed. The release description contains compatibility metadata, automatically generated changes, and installation instructions.

**Validations performed:**
- The `application` field in `version.xml` matches the plugin name
- The `release` field exactly matches the pushed tag without the `v` prefix
- The `date` field matches the current date

**Files excluded from the package:**
`.agents`, `.codex`, `.gitattributes`, `.github`, `.gitignore`, `.gitlab-ci.yml`, `.gitmodules`, `AGENTS.md`, `CLAUDE.md`, `tests`, `cypress`, `resources`, `package.json`, `package-lock.json`, `vite.config.js`, `i18nExtractKeys.vite.js`

#### Usage

In the plugin repository, create `.github/workflows/generate-package.yml`:

```yaml
on:
  push:
    tags:
      - 'v*'

name: Create release and tar.gz package for it

jobs:
  create-release:
    uses: lepidus/github-workflows/.github/workflows/generate-package.yml@main
    with:
      plugin_name: yourPluginName
      pkp_application: OJS
      compatible_versions: OJS 3.5.x
      release_branch: stable-3_5_0
    permissions:
      contents: write
```

#### Requirements

- The repository must have a `version.xml` file at the root with `application`, `release`, and `date` fields
- Tags must follow the `v*` pattern (e.g. `v1.0.0.0`)
- `plugin_name` is required and must match `version/application`
- The compatibility inputs keep release metadata accurate and are strongly recommended:
  - `pkp_application`: compatible PKP application, such as `OJS`, `OMP`, or `OPS`
  - `compatible_versions`: compatible application versions, such as `OJS 3.5.x`
  - `release_branch`: branch from which the release was prepared, such as `stable-3_5_0`
- Existing callers that only pass `plugin_name` remain compatible. Missing compatibility values and the release branch are identified in English as not specified instead of being inferred
- The caller must grant `contents: write` permission so the workflow can create the release and upload its package
