# flake8: noqa ANN201
import argparse
import os
import shutil
import subprocess
import sys
from types import SimpleNamespace
from typing import Optional
from venv import EnvBuilder

VENV_NAME = '.venv'

PLUGIN_DIR = os.getcwd()
ROOT_DIR = os.path.abspath(os.path.join(PLUGIN_DIR, os.pardir))
PLUGIN_NAME = os.path.basename(PLUGIN_DIR)

TEMPLATE_DIR = os.path.abspath(
    os.path.join(os.path.abspath(os.path.dirname(__file__)), "template")
)
TEMPLATE_ROOT_DIR = os.path.join(TEMPLATE_DIR, "root")
TEMPLATE_PLUGIN_DIR = os.path.join(TEMPLATE_DIR, "plugin")

ROOT_FILES = [
    ".qgis-plugin-ci",
    ".pre-commit-config.yaml",
    ".editorconfig",
    "setup.cfg",
    "requirements-dev.txt",
    "README.md",
    "LICENSE",
    ".gitignore",
    "docs/development.md",
    "docs/push_translations.yml",
    "CHANGELOG.md",
    ".github/workflows/tests.yml",
    ".github/workflows/tests_ltr.yml",
    ".github/workflows/release.yml",
    ".github/workflows/pre-commit.yml",
    ".github/ISSUE_TEMPLATE/bug_report.md",
    ".github/ISSUE_TEMPLATE/feature_request.md",
]
PLUGIN_FILES = [
    "test/test_1.py",
    "test/__init__.py",
    "test/pytest.ini",
    "test/conftest.py",
    "metadata.txt",
    "build.py",
    "__init__.py",
    "plugin.py",
    ".gitattributes",
    "resources/ui/.gitignore",
    "resources/i18n/.gitignore",
    "resources/.gitignore",
    "resources/icons/.gitignore",
]


def is_windows():
    return "win" in sys.platform


class QgisEnvBuilder(EnvBuilder):

    def upgrade_dependencies(self, context: SimpleNamespace) -> None:
        """
        Upgrade pip and setuptools and install dependencies and pre-commit.
        post_setup could be used as well, but it will run before upgrade_dependencies,
        which might end up using very old pip.
        :param context:
        :return:
        """
        super(QgisEnvBuilder, self).upgrade_dependencies(context)
        if sys.platform == 'win32':
            python_exe = os.path.join(context.bin_path, 'python.exe')

        else:
            python_exe = os.path.join(context.bin_path, 'python')

        print("Installing requirements")
        requirements = os.path.join(ROOT_DIR, 'requirements-dev.txt')
        cmd = [python_exe, '-m', 'pip', 'install', '-r', requirements]
        subprocess.check_call(cmd)

        print("Setting up pre-commit")
        cmd = [os.path.join(context.bin_path, 'pre-commit'), 'install']
        subprocess.check_call(cmd, cwd=ROOT_DIR)


class PluginCreator:
    def __init__(self, organization: str, repo: str, url: str, python: Optional[str]) -> None:
        self.organization = organization
        self.repo = repo
        self.url = url
        self.python = python

    def create(self):
        os.chdir(TEMPLATE_ROOT_DIR)
        for f in ROOT_FILES:
            self.copy_and_edit_file(ROOT_DIR, f)

        os.chdir(TEMPLATE_PLUGIN_DIR)
        for f in PLUGIN_FILES:
            self.copy_and_edit_file(PLUGIN_DIR, f)

    def create_venv(self):
        if not self.python:
            print("Skipping venv creation")
            return
        env_builder = QgisEnvBuilder(system_site_packages=True, with_pip=True, clear=True, upgrade_deps=True)
        venv_dir = os.path.join(ROOT_DIR, VENV_NAME)
        env_builder.create(venv_dir)

    def copy_and_edit_file(self, dst_dir, f):
        print(f)
        dst_file = os.path.join(dst_dir, f)
        dst_file_dir = os.path.dirname(dst_file)
        if not os.path.exists(dst_file_dir):
            os.makedirs(dst_file_dir)
        shutil.copy2(f, dst_file)
        with open(dst_file) as fil:
            content = fil.read()
        content = (
            content.replace("<plugin_name>", PLUGIN_NAME)
                .replace("<organization>", self.organization)
                .replace("<repo>", self.repo)
                .replace("<url>", self.url)
                .replace("#<commented_out>", "")
                .replace("# <commented_out>", "")  # Automatic formatting might cause these
        )
        with open(dst_file, "w") as fil:
            fil.write(content)


def parse_args():
    parser = argparse.ArgumentParser(prog="PG Initializer")
    parser.add_argument(
        "-o",
        "--organization",
        help="Github / Gitlab organization or user name. "
             "For example GispoCoding in https://github.com/GispoCoding/GlobeBuilder",
        default="",
    )
    parser.add_argument(
        "-r",
        "--repository",
        help="Github / Gitlab repository name. "
             "For example GlobeBuilder in https://github.com/GispoCoding/GlobeBuilder",
        required=True,
    )
    parser.add_argument(
        "-u",
        "--url",
        help="Url of the repository hosting service. "
             "Typically https://github.com or https://gitlab.com",
        default="https://github.com",
    )
    parser.add_argument(
        "-p",
        "--python",
        required=False,
        help="Path to the Python interpreter aware of QGIS."
             "In Windows use the qgis-python.bat shipped with OSGEO4w: "
             r"C:\OSGeo4W64\bin\python-qgis.bat or "
             r"C:\OSGeo4W64\bin\python-qgis-ltr.bat",
    )

    if "-" in PLUGIN_NAME or " " in PLUGIN_NAME:
        raise ValueError(f"Plugin name {PLUGIN_NAME} contains illegal characters")

    return parser.parse_args()


def create_plugin():
    args = parse_args()
    creator = PluginCreator(args.organization, args.repository, args.url, args.python)
    creator.create()
    creator.create_venv()
