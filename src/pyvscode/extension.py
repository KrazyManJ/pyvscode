import re
from dataclasses import dataclass
from typing import Union

from .pyvscode import vscode_check
from re import search, IGNORECASE
from subprocess import run
from os import system as runcmd
from enum import Enum

EXT_STR_REGEX = re.compile("[a-z\d_-]+\.[a-z\d_-]+(@[\d.]+|)", re.IGNORECASE)


class ExtensionCategory(Enum):
    """
    Enum class to filter extensions in function get_installed_extensions()
    """
    AZURE = "azure"
    DEBUGGERS = "debuggers"
    EDUCATION = "education"
    EXTENSION_PACKS = "extension packs"
    FORMATTERS = "formatters"
    KEYMAPS = "keymaps"
    LANGUAGE_PACKS = "language packs"
    LINTERS = "linters"
    MACHINE_LEARNING = "machine learning"
    NOTEBOOKS = "notebooks"
    OTHER = "other"
    PROGRAMMING_LANGUAGES = "programming languages"
    SCM_PROVIDERS = "scm providers"
    SNIPPETS = "snippets"
    TESTING = "testing"
    THEMES = "themes"
    VISUALIZATION = "visualization"


@dataclass(frozen=True)
class VSCodeExtension(object):
    """
    Dataclass for Visual Studio Code Extensions
    """
    publisher: str
    name: str
    version: str

    def __repr__(self) -> str:
        """
        :return: String in format of publisher.name@version
        """
        return f"{self.publisher}.{self.name}@{self.version}"

    def __str__(self) -> str:
        """
        For string with version use repr() method

        :return: String in format of publisher.name
        """
        return f"{self.publisher}.{self.name}"


@vscode_check
def get_installed_extensions(
        category: Union[ExtensionCategory, None] = None
) -> list[VSCodeExtension]:
    """
    Gets list of all Extensions installed in Visual Studio Code.
    Returns list of extensions that are all wrapped in VSCodeExtension dataclass

    :raise NoVSCodeException: If Visual Studio Code is not installed, or it's version does not support CLI (Command Line Interface)
    """
    args = ["code", "--list-extensions", "--show-versions"]
    if category is not None and isinstance(category, ExtensionCategory): args += ["--category", category.value]
    data = run(args, shell=True, capture_output=True).stdout.decode("utf-8", "ignore")
    extensions = []
    for ext in data.split("\n")[:-1]:
        find = search("([a-z\d-]+)\.([a-z0-9-]+)@(.+)", ext, IGNORECASE)
        extensions.append(VSCodeExtension(find.group(1), find.group(2), find.group(3)))
    return extensions


@vscode_check
def install_extension(
        extension: str,
        force: bool = False
) -> None:
    """
    Installs extension in Visual Studio Code.
    Extension in string version must be specified in format `publisher.name`.

    :raise NoVSCodeException: If Visual Studio Code is not installed, or it's version does not support CLI (Command Line Interface)
    """
    if EXT_STR_REGEX.fullmatch(extension) is None:
        raise ValueError("Invalid extension string! String must be formatted as `publisher.name`!")
    runcmd(f"code {'--force' if force else ''} --install-extension {extension}")


@vscode_check
def uninstall_extension(
        extension: str,
        force: bool = False
) -> None:
    """
    Uninstalls extension in Visual Studio Code.
    Extension in string version must be specified in format `publisher.name`.

    :raise NoVSCodeException: If Visual Studio Code is not installed, or it's version does not support CLI (Command Line Interface)
    """
    if EXT_STR_REGEX.fullmatch(extension) is None:
        raise ValueError("Invalid extension string! String must be formatted as `publisher.name`!")
    runcmd(f"code {'--force' if force else ''} --uninstall-extension {extension}")
