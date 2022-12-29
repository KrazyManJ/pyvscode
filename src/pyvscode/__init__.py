"""
Python package for manipulating with the most popular IDE named Visual Studio Code.
Adds ability to open files or folders, open difference
tab between two files and even open file with caret cursor at specific line
and column.

All executed functions are executed from main started script location and without
providing any path, VSCode commands will be executed related to that location.

If Visual Studio Code is not installed on device, or it's version does not support
CLI (Command Line Interface), each attempt of using any method will raise an
NoVSCodeException.

Default keyword arguments for most of the functions:

- new_window - Opens a new session of VS Code instead of restoring the previous session (default).
- reuse_window - Forces opening a file or folder in the last active window.
- locale - Set the display language (locale) for the VS Code session.

"""

from .pyvscode import is_present,NoVSCodeException
from .runner import open,open_folder,open_difference,open_empty_session,VSCodeVersion,get_version,goto_file
from .extension import ExtensionCategory,get_installed_extensions,VSCodeExtension,uninstall_extension,install_extension
