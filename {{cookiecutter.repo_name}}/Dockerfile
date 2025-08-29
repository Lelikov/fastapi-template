ARG BASE_IMAGE="python:{{cookiecutter.python_version}}-slim"

FROM ${BASE_IMAGE} AS base

ENV HOME_PATH="/home/{{cookiecutter.project_name}}"

ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.2 \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1

ENV PATH="${POETRY_HOME}/bin:${HOME_PATH}/.venv/bin:${PATH}"

WORKDIR ${HOME_PATH}

FROM base AS deps

RUN apt-get update && \
    apt-get install -y \
    curl

RUN --mount=type=cache,target=/root/.cache \
    curl -sSL https://install.python-poetry.org | python -

WORKDIR ${HOME_PATH}
COPY poetry.lock pyproject.toml ./
RUN --mount=type=cache,target=/root/.cache \
    poetry config installer.max-workers 10 && \
    poetry config virtualenvs.in-project true && \
    poetry install --no-dev

FROM deps AS development

RUN groupadd -g 1000 {{cookiecutter.project_name}} \
    && useradd -u 1000 -g {{cookiecutter.project_name}} \
    -d ${HOME_PATH} -m -s /bin/bash {{cookiecutter.project_name}}
WORKDIR ${HOME_PATH}
USER {{cookiecutter.project_name}}

COPY --from=deps --chown=1000:1000 ${HOME_PATH}/.venv ${HOME_PATH}/.venv
COPY --chown=1000:1000 {{cookiecutter.project_name}} {{cookiecutter.project_name}}

ENTRYPOINT ["uvicorn", "{{cookiecutter.project_name}}.__main__:APP"]
