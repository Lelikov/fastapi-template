{%- if cookiecutter.is_service_with_database %}
from {{cookiecutter.project_name}}.controllers.db import DbController
{%- endif %}
