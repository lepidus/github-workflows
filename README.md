# github-workflows

**English** | [Português Brasileiro](/lepidus/github-workflows/blob/main/docs/README-pt_BR.md) | [Español](/lepidus/github-workflows/blob/main/docs/README-es.md)

Reusable GitHub Actions workflows for Lepidus plugins.

## Available workflows

### `generate-package.yml`

Validates `version.xml` and generates a `.tar.gz` package as a release asset when a tag is pushed.

**Validations performed:**
- The `application` field in `version.xml` matches the plugin name
- The `release` field matches the pushed tag
- The `date` field matches the current date

**Files excluded from the package:**
`tests`, `cypress`, `resources`, `CLAUDE.md`, `package.json`, `package-lock.json`, `vite.config.js`, `i18nExtractKeys.vite.js`

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
```

#### Requirements

- The repository must have a `version.xml` file at the root with `application`, `release`, and `date` fields
- Tags must follow the `v*` pattern (e.g. `v1.0.0.0`)
