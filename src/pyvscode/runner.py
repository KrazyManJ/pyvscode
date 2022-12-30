from dataclasses import dataclass
from subprocess import run
from os import system as runcmd, PathLike
from os.path import join as joinpath
from typing import Union

from .pyvscode import vscode_check


def __opt__(**kwargs):
    ret = ""
    if kwargs.get("new_window", False): ret += "-n"
    if kwargs.get("reuse_window", False): ret += " -r"
    if kwargs.get("locale", None) is not None: ret += " --locale " + kwargs["locale"]
    return ret


def __islistinstance(obj, cls_or_tuple):
    return all(isinstance(p, cls_or_tuple) for p in obj)


@vscode_check
def open(paths, new_window=False, reuse_window=False, locale=None):
    """
    Opens one file, folder or multiple files in VS Code editor.
    Allows to open files that don't even exists. To open a folder, the folder needs to exist.

    :raise NoVSCodeException: If Visual Studio Code is not installed, or it's version does not support CLI (Command Line Interface)
    """
    if isinstance(paths, list) and not __islistinstance(paths, Union[str, bytes, PathLike]):
        raise TypeError("List with unexpected type, expected PathLike string!")
    if not isinstance(paths, list) and not isinstance(paths, Union[str, bytes, PathLike]):
        raise TypeError(f"Expected PathLike string, got {type(paths)} instead!")
    files = paths if type(paths) is str else " ".join(paths)
    runcmd(f'code {__opt__(new_window=new_window, reuse_window=reuse_window, locale=locale)} {files}')


@vscode_check
def open_difference(first_file_path, second_file_path, new_window=False, reuse_window=False, locale=None):
    """
    Opens difference tab between two files in Visual Studio Code.

    :raise NoVSCodeException: If Visual Studio Code is not installed, or it's version does not support CLI (Command Line Interface)
    """
    if not isinstance(first_file_path, Union[str, bytes, PathLike]):
        raise TypeError(f"First path incorrect type, expected PathLike string, got {type(first_file_path)} instead!")
    if not isinstance(second_file_path, Union[str, bytes, PathLike]):
        raise TypeError(f"Second path incorrect type, expected PathLike string, got {type(first_file_path)} instead!")
    runcmd(
        f"code -d {__opt__(new_window=new_window, reuse_window=reuse_window, locale=locale)} {first_file_path} {second_file_path}")


@vscode_check
def goto_file(file_path, line, character=None, new_window=False, reuse_window=False, locale=None):
    """
    Opens specific file with caret cursor at specific line and column (character) in Visual Studio Code.
    In default caret position is [1;1] (start of the file)

    :raise NoVSCodeException: If Visual Studio Code is not installed, or it's version does not support CLI (Command Line Interface)
    """
    if not isinstance(file_path, Union[str, bytes, PathLike]):
        raise TypeError(f"Expected PathLike string, got {type(file_path)} instead!")
    if type(line) is not int:
        raise TypeError(f"Line must be an integer, not {type(line)}!")
    if character is not None and type(character) is not int:
        raise TypeError(f"Character must be an integer, not {type(line)}!")
    char = f":{str(character)}" if character is not None else ""
    runcmd(
        f"code -g {__opt__(new_window=new_window, reuse_window=reuse_window, locale=locale)} {file_path}:{line}{char}")


@vscode_check
def open_empty_session(locale=None):
    """
    Shorthand for `open()` method. Opens new Visual Studio Code with empty session.

    :raise NoVSCodeException: If Visual Studio Code is not installed, or it's version does not support CLI (Command Line Interface)
    """
    open("", True, locale=locale)


@vscode_check
def open_folder(folder_path, files_path=None, new_window=False, reuse_window=False, locale=None):
    """
    Shorthand for `open()` method.
    Opens a folder in Visual Studio Code, in addition rather than classic `open()` method
    it can also open multiple files in relative path to opened folder.

    :raise NoVSCodeException: If Visual Studio Code is not installed, or it's version does not support CLI (Command Line Interface)
    """
    paths = [joinpath(folder_path, path) for path in files_path] if files_path is not None else []
    paths.insert(0, folder_path)
    open(paths, new_window, reuse_window, locale)


@dataclass(frozen=True, eq=True)
class VSCodeVersion:
    """
    Dataclass for Visual Studio Code version. Contains version, Github commit ID and architecture detail.
    """
    version: str
    github_commit_id: str
    architecture: str

    def __str__(self): return self.version


@vscode_check
def get_version():
    """
    Gets Visual Studio Code version that is installed

    :raise NoVSCodeException: If Visual Studio Code is not installed, or it's version does not support CLI (Command Line Interface)
    """
    data = run(["code", "-v"], shell=True, capture_output=True).stdout.decode("utf-8", "ignore").split("\n")[:-1]
    return VSCodeVersion(data[0], data[1], data[2])  # type: ignore
