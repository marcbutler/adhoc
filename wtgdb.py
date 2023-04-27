#
# Provides a gdb command wt-setenv that will attempt to infer and setup
# shared library path and source code path substitution.
#
# The command assumes you are running gdb in a subdirectory of an unpacked
# artifact and walks up (down?) the directory structure, based on the 
# assumption the relevant information and paths are in parent directories.
#  
# To use load the file in gdb:
#   (gdb) source /path/to/wtgdb.py
#
# TODO Look for TCMALLOC shared library and add that directory to the so-lib
#   search path.
# 
# TODO Check gdb variables before overwriting them.
#
# TODO Provide functionality to save settings in a gdbinit file in the 
#   current directory.
#
# TODO Potentially look above the artifact level for a possible source
#   code directory.

import gdb
import re
import os, os.path


def parent_dir(path):
    if path == '/':
        raise RuntimeError('parent_dir() called on root')
    return os.path.join(*os.path.split(path)[:-1])


def parse_stacktrace_for_source_dir(path):
    """Look for a reference to wired tiger code in the dump file stacktrace and
    return the root directory for the source."""

    with open(path, 'r') as trace:
        for line in trace.readlines():
            if m := re.match(r'.* at (/.*/wiredtiger)/src/.*:\d+$', line):
                return m.group(1)
    return None


def try_infer_source_root(path):
    """If the directory path provided contains CI generated stack trace files,
    inspect them to identify the expected source root directory.

    If more than one stack trace file exists in the directory the first valid 
    looking source path encountered will be the path returned. Searching does
    not continue after the first possible value is encountered."""

    for f in os.listdir(path):
        if not re.match(r'^dump_\w+\.\d+\.stacktrace\.txt$', f):
            continue
        if src_dir := parse_stacktrace_for_source_dir(os.path.join(path, f)):
            return src_dir
    return None


def check_for_solib_dir(path):
    """If the directory path provided contains the wiredtiger shared
    object: return the full path; otherwise return None."""

    for f in os.listdir(path):
        if not re.match(r'^libwiredtiger.so*', f):
            continue
        full_path = os.path.join(path, f)
        if os.path.isfile(full_path):
            return path
    return None


def find_probable_src_dir(path):
    """Look for a parent directory containing the subdirectory 'src',
    and if found return the directory path."""
    while path != '/':
        if os.path.isdir(os.path.join(path, 'src')):
            return path
        path = parent_dir(path)
    return None

 
class WiredTigerSetEnv(gdb.Command):
    """Automatically setup working environment."""
    def __init__(self, cmd):
        super(WiredTigerSetEnv, self).__init__(cmd, gdb.COMMAND_USER)

    def complete(self, text, word):
        return gdb.COMPLETE_SYMBOL

    def invoke(self, args, from_tty):
        solib_path, inferred_src_root = None, None
        path = os.getcwd()
        while path != '/' and solib_path == None and inferred_src_root == None:
            if solib_path == None:
               solib_path = check_for_solib_dir(path)
            if inferred_src_root == None:
               inferred_src_root = try_infer_source_root(path)
            path = parent_dir(path)

        if solib_path:
            gdb.set_parameter("solib-search-path", solib_path)
            print("solib-search-path = {0}".format(solib_path))
        else:
            print("libwiredtiger.so not found: could not set solib-search-path")

        if inferred_src_root and not os.path.isdir(inferred_src_root):
            print("Source root dir does not exist: {0}".format(inferred_src_root))
            src_dir = find_probable_src_dir(path)
            if src_dir:
                print("substitute-path = {0}".format(src_dir))
                gdb.set_parameter("substitute-path", " ".join((inferred_src_root, src_dir)))
            else:
                print("Unable to find a substitute source path.")
        else:
            print("Could not infer source root directory.")

        return None


# Register commands.
WiredTigerSetEnv("wt-setenv")
