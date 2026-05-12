# agrobase

Base package for Python projects in the Biotrop / AgroReporter environment.
Provides a small set of cross-cutting building blocks:

- `Either[Left, Right]` monad (`agrobase.either`)
- `MappedErrors` hierarchy + `ErrorCodes` enum (`agrobase.exceptions`)
- Abstract response shapes — `CreateResponse`, `FetchResponse`, …
  (`agrobase.entities`)
- File-based lock helpers (`agrobase.lock`)
- Slugify / coercion validators (`agrobase.validations`)
- Singleton Prisma client wrapper (`agrobase.connectors.prisma_connector`)
- Bio-archival assay fetcher + DTOs
  (`agrobase.connectors.bio_archival`)
- Domain enums: `CropEnum`, `GroupEnum`, `TaxaEnum`, `InferenceSourceEnum`

## Consumption

`agrobase` is consumed as a **git submodule** by sibling repositories
in the monorepo. The canonical setup, on the consumer side, looks like:

```bash
# consumer repo (e.g. agroindex-api):
git submodule add https://github.com/Biotrop/agrobase-py.git modules/agrobase-py
git submodule update --init --recursive
```

And in the consumer's `pyproject.toml`:

```toml
[tool.poetry.dependencies]
agrobase = { path = "modules/agrobase-py", develop = true }
```

Run `poetry install` and `agrobase` resolves from the submodule directory.

To bump the pinned revision later:

```bash
git submodule update --remote --merge modules/agrobase-py
poetry lock
poetry install
git add modules/agrobase-py poetry.lock
git commit -m "chore(deps): bump agrobase to <new-sha>"
```

## Development

```bash
# install dev tooling (Pipenv)
pipenv install --dev

# run tests
pipenv run test
```

## Versioning

[Commitizen](https://github.com/commitizen-tools/commitizen) drives
semver bumps from Conventional Commits.

```bash
cz bump --check-consistency --changelog --dry-run   # preview
cz bump --increment PATCH                            # 2.2.x → 2.2.(x+1)
cz bump --increment MINOR                            # 2.2.x → 2.3.0
cz bump --increment MAJOR                            # 2.2.x → 3.0.0
```

The bump tags the commit and refreshes `CHANGELOG.md`. Push the
resulting commit + tag.
