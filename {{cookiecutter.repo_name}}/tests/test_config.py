"""Tests for {{cookiecutter.project_title}} config."""

from {{cookiecutter.project_name}}.config import Settings
from tests.conftest import patch_settings_context


INSENSITIVE_SETTINGS: set[str] = {
    "log_level",
    {%- if cookiecutter.is_service_with_database %}
    "postgres_pool_min_size",
    "postgres_pool_max_size",
    {%- endif %}
}


def test_config() -> None:
    """Test config."""
    unmasked_settings: set[str] = set()
    with patch_settings_context():
        for setting in str(Settings()).split(", "):
            key, value = setting.split(": ")
            if value != "***":
                unmasked_settings.add(key)

    assert unmasked_settings == INSENSITIVE_SETTINGS
