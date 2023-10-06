def is_present():
    """
    Checks if Visual Studio Code is installed. Is runned everytime, when you try to perform
    any action from pyvscode.
    """
    from subprocess import run, CREATE_NO_WINDOW
    return run(["code", "-v"], shell=True, capture_output=True, creationflags=CREATE_NO_WINDOW).returncode == 0


class NoVSCodeException(Exception):
    """
    Exception thrown everytime when you attempt to use pyvscode while Visual Studio Code is not installed
    """
    __module__ = Exception.__module__

    def __init__(self) -> None:
        if is_present(): return
        super().__init__("Visual Studio Code was not found on this computer!")


def vscode_check(func):
    def inner(*args, **kwargs):
        if not is_present():
            raise NoVSCodeException()
        return func(*args, **kwargs)

    return inner
