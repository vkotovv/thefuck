from difflib import get_close_matches
from thefuck.shells import shell
from thefuck.utils import get_closest, memoize, get_all_executables, get_alias


def _not_corrected(history, tf_alias):
    """Returns all lines from history except that comes before `fuck`."""
    previous = None
    for line in history:
        if previous is not None and line != tf_alias:
            yield previous
        previous = line
    if history:
        yield history[-1]


@memoize
def _history_of_exists_without_current(command):
    history = shell.get_history()
    tf_alias = get_alias()
    executables = get_all_executables()
    return [line for line in _not_corrected(history, tf_alias)
            if not line.startswith(tf_alias) and not line == command.script
            and line.split(' ')[0] in executables]


def match(command):
    return len(get_close_matches(command.script,
                                 _history_of_exists_without_current(command)))


def get_new_command(command):
    return get_closest(command.script,
                       _history_of_exists_without_current(command))


priority = 9999
