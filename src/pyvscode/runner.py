from dataclasses import dataclass
from subprocess import run
from os import system as runcmd, PathLike
from os.path import join as joinpath
from typing import Union, Iterable, Literal

from .pyvscode import is_present, NoVSCodeException


def __opt__(**kwargs):
    ret = ""
    if kwargs.get("new_window", False): ret += "-n"
    if kwargs.get("reuse_window", False): ret += " -r"
    if kwargs.get("locale", None) is not None: ret += " --locale " + kwargs["locale"]
    return ret


def open(
        paths: Union[str, bytes, PathLike, Iterable[Union[str, bytes, PathLike]]],
        new_window: bool = False,
        reuse_window: bool = False,
        locale: Union[Literal[
            "en", "zh-cn", "zh-tw", "fr", "de", "it", "es", "ja", "ko", "ru", "pt-br", "tr", "pl", "cs"], None] = None
) -> None:
    """
    Opens one file, folder or multiple files in VS Code editor.
    Allows to open files that don't even exists. To open a folder, the folder needs to exist.

    :raise NoVSCodeException: If Visual Studio Code is not installed, or it's version does not support CLI (Command Line Interface)
    """
    if not is_present(): return
    files = paths if type(paths) is str else " ".join(paths)
    runcmd(f'code {__opt__(new_window=new_window, reuse_window=reuse_window, locale=locale)} {files}')


def open_difference(
        first_file_path: Union[str, bytes, PathLike],
        second_file_path: Union[str, bytes, PathLike],
        new_window: bool = False,
        reuse_window: bool = False,
        locale: Union[Literal[
            "en", "zh-cn", "zh-tw", "fr", "de", "it", "es", "ja", "ko", "ru", "pt-br", "tr", "pl", "cs"], None] = None
) -> None:
    """
    Opens difference tab between two files in Visual Studio Code.

    :raise NoVSCodeException: If Visual Studio Code is not installed, or it's version does not support CLI (Command Line Interface)
    """
    if not is_present(): return
    runcmd(
        f"code -d {__opt__(new_window=new_window, reuse_window=reuse_window, locale=locale)} {first_file_path} {second_file_path}")


def goto_file(
        file_path: Union[str, bytes, PathLike],
        line: int,
        character: Union[int, None] = None,
        new_window: bool = False,
        reuse_window: bool = False,
        locale: Union[Literal[
            "en", "zh-cn", "zh-tw", "fr", "de", "it", "es", "ja", "ko", "ru", "pt-br", "tr", "pl", "cs"], None] = None
) -> None:
    """
    Opens specific file with caret cursor at specific line and column (character) in Visual Studio Code.
    In default caret position is [1;1] (start of the file)

    :raise NoVSCodeException: If Visual Studio Code is not installed, or it's version does not support CLI (Command Line Interface)
    """
    if not is_present(): return
    runcmd(
        f"code -g {__opt__(new_window=new_window, reuse_window=reuse_window, locale=locale)} {file_path}:{line}{':' + str(character) if character is not None else ''}")


def open_empty_session(
        locale: Union[Literal[
            "en", "zh-cn", "zh-tw", "fr", "de", "it", "es", "ja", "ko", "ru", "pt-br", "tr", "pl", "cs"], None] = None
) -> None:
    """
    Shorthand for `open()` method. Opens new Visual Studio Code with empty session.

    :raise NoVSCodeException: If Visual Studio Code is not installed, or it's version does not support CLI (Command Line Interface)
    """
    if not is_present(): return
    open("", True, locale=locale)


def open_folder(
        folder_path: Union[str, bytes, PathLike],
        files_path: Union[Iterable[Union[str, bytes, PathLike]],] = None,
        new_window: bool = False,
        reuse_window: bool = False,
        locale: Union[Literal[
            "en", "zh-cn", "zh-tw", "fr", "de", "it", "es", "ja", "ko", "ru", "pt-br", "tr", "pl", "cs"], None] = None
) -> None:
    """
    Shorthand for `open()` method.
    Opens a folder in Visual Studio Code, in addition rather than classic `open()` method
    it can also open multiple files in relative path to opened folder.

    :raise NoVSCodeException: If Visual Studio Code is not installed, or it's version does not support CLI (Command Line Interface)
    """
    if not is_present(): return
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


def get_version() -> VSCodeVersion:
    """
    Gets Visual Studio Code version that is installed

    :raise NoVSCodeException: If Visual Studio Code is not installed, or it's version does not support CLI (Command Line Interface)
    """
    if not is_present(): raise NoVSCodeException()
    data = run(["code", "-v"], shell=True, capture_output=True).stdout.decode("utf-8", "ignore").split("\n")[:-1]
    return VSCodeVersion(data[0], data[1], data[2])  # type: ignore
