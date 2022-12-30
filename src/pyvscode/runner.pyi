from os import PathLike
from typing import Iterable, Literal, Union

__LOCALES__ = Literal["en", "zh-cn", "zh-tw", "fr", "de", "it", "es", "ja", "ko", "ru", "pt-br", "tr", "pl", "cs"]


def open(
        paths: Union[str, bytes, PathLike, Iterable[Union[str, bytes, PathLike]]],
        new_window: bool = ...,
        reuse_window: bool = ...,
        locale: Union[__LOCALES__, None] = ...
) -> None: ...


def open_difference(
        first_file_path: Union[str, bytes, PathLike],
        second_file_path: Union[str, bytes, PathLike],
        new_window: bool = ...,
        reuse_window: bool = ...,
        locale: Union[__LOCALES__, None] = None
) -> None: ...


def goto_file(
        file_path: Union[str, bytes, PathLike],
        line: int = ...,
        character: Union[int, None] = ...,
        new_window: bool = ...,
        reuse_window: bool = ...,
        locale: Union[__LOCALES__, None] = ...
) -> None: ...


def open_empty_session(
        locale: Union[__LOCALES__, None] = ...
) -> None: ...


def open_folder(
        folder_path: Union[str, bytes, PathLike],
        files_path: Union[Iterable[Union[str, bytes, PathLike]], None] = ...,
        new_window: bool = ...,
        reuse_window: bool = ...,
        locale: Union[__LOCALES__, None] = ...
) -> None: ...


def get_version() -> VSCodeVersion: ...


class VSCodeVersion(object):
    version: str
    github_commit_id: str
    architecture: str
