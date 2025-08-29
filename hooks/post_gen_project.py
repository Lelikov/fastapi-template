import os
import shutil
import sys
from decimal import Decimal
import subprocess


def _replace_content_in_files(file_names: list[str], replace_data: dict[str, str]):
    for file_name in file_names:
        with open(file_name) as f:
            contents = f.read()
            for template, value in replace_data.items():
                contents = contents.replace(rf"{template}", value)
        with open(file_name, "w") as f:
            f.write(contents)


def set_python_version():
    python_version = "{{ cookiecutter.python_version }}"
    next_minor_python_version = (Decimal(python_version) + Decimal(0.01)).quantize(Decimal(".01"))
    _replace_content_in_files(file_names=["pyproject.toml"], replace_data={"{python_version}": python_version})
    _replace_content_in_files(file_names=["pyproject.toml"], replace_data={"{next_minor_python_version}": str(next_minor_python_version)})


def set_python_image_version():
    python_image_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    _replace_content_in_files(file_names=["Dockerfile","README.md"], replace_data={"{python_image_ver}": python_image_ver})


def set_python_version_without_dot():
    python_ver_without_dot = "{{ cookiecutter.python_version }}".replace(".", "")
    _replace_content_in_files(file_names=["pyproject.toml"], replace_data={"{python_ver_without_dot}": python_ver_without_dot})


def delete_db_files():
    is_service_with_database = "{{ cookiecutter.is_service_with_database }}"
    project_dir = "{{cookiecutter.project_name}}"
    if is_service_with_database == "False":
        print(INFO + "Removing database files" + TERMINATOR)
        shutil.rmtree(f"{project_dir}/adapters/db")
        shutil.rmtree(f"{project_dir}/controllers/db")
        shutil.rmtree(f"tests/adapters/db")
        os.remove(f"tests/fixtures/db.py")


def delete_all_api_portal_files():
    is_service_will_be_published_on_api_portal = "{{ cookiecutter.is_service_will_be_published_on_api_portal }}"
    if not is_service_will_be_published_on_api_portal:
        os.remove("mkdocs.yaml")
        os.remove("catalog-info.yaml.bak")
        shutil.rmtree("docs")


def freeze_poetry_packages():
    is_freeze_poetry_packages = True if "{{ cookiecutter.is_freeze_poetry_packages }}" == "True" else False
    if is_freeze_poetry_packages:
        print(INFO + "Starting package updates" + TERMINATOR)
        try:
            subprocess.run(args=["poetry", "up", "--latest"], check=True)
            print(SUCCESS + "The packages have been successfully frozen" + TERMINATOR)
        except FileNotFoundError:
            print(INFO + "Poetry not found. Unable to freeze package versions" + TERMINATOR)
        except subprocess.CalledProcessError:
            print(INFO + "Plugin Up for Poetry not found. Install it `poetry self add poetry-plugin-up`" + TERMINATOR)


SUCCESS = "\x1b[1;32m"
INFO = "\x1b[1;33m"
TERMINATOR = "\x1b[0m"


def main():
    set_python_version()
    set_python_image_version()
    set_python_version_without_dot()
    delete_db_files()
    delete_all_api_portal_files()
    print(SUCCESS + "Project successfully initialized" + TERMINATOR)
    freeze_poetry_packages()


if __name__ == "__main__":
    main()
