# Python Best Practices Cookiecutter

Best practices cookiecutter template for Python projects.

## 🎯 Features

- **Testing** with [pytest](https://docs.pytest.org/en/latest/)
- **Static typing** with [mypy](http://mypy-lang.org/)
- **Linting and formating** with [ruff](https://beta.ruff.rs/docs/)
- **Dependency management** with [Poetry](https://python-poetry.org/)
- **Pre-commit hooks** for code quality
- **Docker** support

## 🚀 Quickstart

```sh
# Install pipx, poetry and cookiecutter if not installed
python3 -m pip install pipx
pipx install cookiecutter
pipx install poetry
poetry self add poetry-plugin-up

# Use cookiecutter to create project from this template
cookiecutter .

# Enter project directory
cd <repo_name>

# Initialise git repo
git init

# Setup pre-commit and pre-push hooks
poetry run pre-commit install -t pre-commit
poetry run pre-commit install -t pre-push
```

## 📋 Option Descriptions

### Basic Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `repo_name` | `best-practices` | Repository name. Used to create the repository name and generate other parameters. Recommended to use kebab-case (e.g., `my-awesome-project`) |
| `project_title` | *auto-generated* | Project title. Automatically generated from `repo_name` by replacing hyphens with spaces and applying Title Case<br/>**Example:** `best-practices` → `Best Practices` |
| `project_name` | *auto-generated* | Project name for use in code. Automatically generated from `repo_name` by replacing hyphens with underscores. Used for imports and module names<br/>**Example:** `best-practices` → `best_practices` |
| `pascal_case_project_name` | *auto-generated* | Project name in PascalCase. Automatically generated from `project_title` by removing spaces. Used for class names and other elements requiring PascalCase<br/>**Example:** `Best Practices` → `BestPractices` |

### Technical Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `python_version` | `3.12` | Defines the minimum Python version for the project. Used in pyproject.toml and other configuration files |

### Functional Options

| Parameter | Options | Description                                                                                                                                                                                                                              |
|-----------|---------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `is_service_with_database` | `[true, false]` | **Enable database support**<br/>• `true` - adds configuration for working with databases (ORM, migrations, etc.)<br/>• `false` - creates a project without database support                                                              |
| `is_service_will_be_published_on_api_portal` | `[true, false]` | **Publish to API portal [Backstage](https://github.com/backstage/backstage/tree/master)**<br/>• `true` - adds necessary configurations and documentation for API publishing<br/>• `false` - creates a project without API portal support |
| `is_freeze_poetry_packages` | `[true, false]` | **Freeze Poetry packages**<br/>• `true` - creates poetry.lock with fixed dependency versions<br/>• `false` - uses flexible dependency versions for development                                                                           |

# 🌍 Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR) | `DEBUG` | No |

Database Configuration
Available when `is_service_with_database` is `true`

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `POSTGRES_DSN` | PostgreSQL Data Source Name (connection string) | -       | Yes |
| `POSTGRES_POOL_MIN_SIZE` | Minimum number of connections in the connection pool | 5       | No |
| `POSTGRES_POOL_MAX_SIZE` | Maximum number of connections in the connection pool | 20      | No |


# 🐳 Docker Usage

## Build image
`docker build -t <project_name> .`

## Run container
`docker run -p 8000:8000 --env-file .env <project_name>`

## Run container with database
`docker-compose up`

## Run tests
`docker-compose run --rm app poetry run pytest`

# 🔍 Code Quality with Ruff

This project uses [Ruff](https://beta.ruff.rs/docs/) as a fast Python linter and code formatter, replacing multiple tools like flake8, isort, and others.

## Formatting Code

Format your code according to project standards:

```sh
# Format all Python files in the current directory
ruff format .

# Format specific file
ruff format __main__.py

# Check what would be formatted without making changes
ruff format --check .
```

## Linting Code

```sh
# Check for linting issues and automatically fix them
ruff check --fix

# Check for linting issues without fixing
ruff check .

# Check specific file
ruff check __main__.py

# Show all available rules
ruff linter
```