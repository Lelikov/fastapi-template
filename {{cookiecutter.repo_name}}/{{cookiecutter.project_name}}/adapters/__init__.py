{%- if cookiecutter.is_service_with_database %}
from {{cookiecutter.project_name}}.adapters.db import DBWithRetries
{%- endif %}
