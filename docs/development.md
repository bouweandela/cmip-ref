[](){#development-reference}
# Development

Notes for developers. If you want to get involved, please do!
We welcome all kinds of contributions, for example:

- docs fixes/clarifications
- bug reports
- bug fixes
- feature requests
- pull requests
- tutorials

## Development Installation

For development, we rely on [uv](https://docs.astral.sh/uv) for all our
dependency management. To get started, you will need to make sure that uv
is installed
([instructions here](https://docs.astral.sh/uv/getting-started/installation/)).

We use our `Makefile` to provide an easy way to run common developer commands.
You can read the instructions out and run the commands by hand if you wish,
but we generally discourage this because it can be error prone.

The following steps are required to set up a development environment.
This will install the required dependencies and fetch some test data,
as well as set up the configuration for the REF.

```bash
# Create a virtual environment containing the REF and its dependencies.
make virtual-environment

# Configure the REF.
mkdir $PWD/.ref
uv run ref config list > $PWD/.ref/ref.toml
export REF_CONFIGURATION=$PWD/.ref

# Download some test data and ingest the sample datasets.
make fetch-test-data
uv run ref datasets ingest --source-type cmip6 $PWD/tests/test-data/sample-data
```

`uv` will create a virtual Python environment in the directory `.venv` containing
the REF and its (development) dependencies.
To use the software installed in this environment without starting every command
with `uv run`, activate it by calling `. .venv/bin/activate`.
It can be deactivated with the command `deactivate`.

The local `ref.toml` configuration file will make it easier to play around with settings.
By default, the database will be stored in your home directory,
this can be modified by changing the `db.database_url` setting in the `ref.toml` file.

If there are any issues, the messages from the `Makefile` should guide you
through. If not, please raise an issue in the
[issue tracker](https://github.com/CMIP-REF/cmip-ref/issues).

### Pip editable installation

If you would like to install the REF into an existing (conda) environment
without using `uv`, run the command

```bash
for package in packages/cmip_ref_core packages/cmip_ref packages/cmip_ref_metrics-*; do
     pip install -e $package;
done
```

## Tests and code quality

The test suite can then be run using `make test`.
This will run the test suites for each package and finally the integration test suite.

We make use of [`ruff`](https://docs.astral.sh/ruff/) (code formatting and
linting) and [`mypy`](https://mypy.readthedocs.io/en/stable/) (type checking)
and [`pre-commit`](https://pre-commit.com/) (checks before committing) to
maintain good code quality.

These tools can be run as usual after activating the virtual environment or
using the makefile:

```bash
make pre-commit
make mypy
make test
```

## Documentation

Our documentation is written in Markdown and built using
[`mkdocs`](https://www.mkdocs.org/).
It can be viewed while editing by running `make docs-serve`.

It is hosted by
[Read the Docs (RtD)](https://www.readthedocs.org/),
a service for which we are very grateful.
The RtD configuration can be found in the `.readthedocs.yaml` file
in the root of this repository.
The docs are automatically deployed at
[cmip-ref.readthedocs.io](https://cmip-ref.readthedocs.io/en/latest/).

## Workflows

We don't mind whether you use a branching or forking workflow.
However, please only push to your own branches,
pushing to other people's branches is often a recipe for disaster,
is never required in our experience
so is best avoided.

Try and keep your pull requests as small as possible
(focus on one thing if you can).
This makes life much easier for reviewers
which allows contributions to be accepted at a faster rate.

## Language

We use British English for our development.
We do this for consistency with the broader work context of our lead developers.

## Versioning

This package follows the version format
described in [PEP440](https://peps.python.org/pep-0440/)
and [Semantic Versioning](https://semver.org/)
to describe how the version should change
depending on the updates to the code base.

Our changelog entries and compiled [changelog](./changelog.md)
allow us to identify where key changes were made.

## Changelog

We use [towncrier](https://towncrier.readthedocs.io/en/stable/)
to manage our changelog which involves writing a news fragment
for each Merge Request that will be added to the [changelog](./changelog.md) on the next release.
See the [changelog](https://github.com/CMIP-REF/cmip-ref/tree/main/changelog) directory
for more information about the format of the changelog entries.

## Dependency management

We manage our dependencies using [uv](https://docs.astral.sh/uv/).
This allows the ability to author multiple packages in a single repository,
and provides a consistent way to manage dependencies across all of our packages.
This mono-repo approach might change once the packages become more mature,
but since we are in the early stages of development,
there will be a lot of refactoring of the interfaces to find the best approach.

## Database management

The REF uses a local Sqlite database to store state information.
We use [alembic](https://alembic.sqlalchemy.org/en/latest/) to manage our database migrations
as the schema of this database changes.

When making changes to the database models (`cmip_ref.models`),
a migration must also be added (see below).

The migration definitions (and the alembic configuration file)
are included in the `cmip_ref` package (`packages/ref/src/cmip_ref/migrations`)
to enable users to apply these migrations transparently.
Any new migrations are performed automatically when using the `ref` command line tool.

### Adding a database migration

If you have made changes to the database models,
you will need to create a new migration to apply these changes.
Alembic can autogenerate these migrations for you,
but they will need to be reviewed to ensure they are correct.

```
uv run alembic -c packages/ref/src/cmip_ref/alembic.ini \
   revision --autogenerate --message "your_migration_message"
```

[](){releasing-reference}
## Releasing

Releasing is semi-automated via a CI job.
The CI job requires the type of version bump
that will be performed to be manually specified.
The supported bump types are:

* `major`
* `minor`
* `patch`

We don't yet support pre-release versions,
but this is something that we will consider in the future.

### Standard process

The steps required are the following:

1. Bump the version: manually trigger the "bump" workflow from the main branch
   (see here: [bump workflow](https://github.com/CMIP-REF/cmip-ref/actions/workflows/bump.yaml)).
   A valid "bump_rule" will need to be specified.
   This will then trigger a draft release.

1. Edit the draft release which has been created
   (see here:
   [project releases](https://github.com/CMIP-REF/cmip-ref/releases)).
   Once you are happy with the release (removed placeholders, added key
   announcements etc.) then hit 'Publish release'. This triggers the `release` workflow to
   PyPI (which you can then add to the release if you want).


1. That's it, release done, make noise on social media of choice, do whatever
   else

1. Enjoy the newly available version
