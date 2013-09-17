"""Base text style definitions"""
#
# Bold and text reset switches
#
RESET = '\033[0m'
BOLD  = '\033[1m'

#
# Terminal colors
#
# Using regular terminal colors for the _DARK versions, and high intensity
# colors (which are similar to bold colors but without the boldness) for the
# normal versions of each color.
#
# References:
# http://en.wikipedia.org/wiki/ANSI_escape_code
# https://wiki.archlinux.org/index.php/Color_Bash_Prompt
#
_LIGHT = '\033[0;9%dm'
_DARK  = '\033[0;3%dm'

FOREGROUND   = _LIGHT % 7
RED_DARK     = _DARK  % 1
RED          = _LIGHT % 1
GREEN_DARK   = _DARK  % 2
GREEN        = _LIGHT % 2
YELLOW_DARK  = _DARK  % 3
YELLOW       = _LIGHT % 3
BLUE_DARK    = _DARK  % 4
BLUE         = _LIGHT % 4
MAGENTA_DARK = _DARK  % 5
MAGENTA      = _LIGHT % 5
CYAN_DARK    = _DARK  % 6
CYAN         = _LIGHT % 6
LIGHTGREY    = _DARK  % 7
WHITE        = _LIGHT % 7