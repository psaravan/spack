##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://scalability-llnl.github.io/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import sys
import os
import textwrap
from StringIO import StringIO

from llnl.util.tty.color import *

_debug   = False
_verbose = False
indent  = "  "

def set_debug(flag):
    global _debug
    _debug = flag


def set_verbose(flag):
    global _verbose
    _verbose = flag


def msg(message, *args):
    cprint("@*b{==>} %s" % cescape(message))
    for arg in args:
        print indent + str(arg)


def info(message, *args, **kwargs):
    format = kwargs.get('format', '*b')
    stream = kwargs.get('stream', sys.stdout)

    cprint("@%s{==>} %s" % (format, cescape(str(message))), stream=stream)
    for arg in args:
        lines = textwrap.wrap(
            str(arg), initial_indent=indent, subsequent_indent=indent)
        for line in lines:
            stream.write(line + '\n')


def verbose(message, *args):
    if _verbose:
        info(message, *args, format='c')


def debug(message, *args):
    if _debug:
        info(message, *args, format='g', stream=sys.stderr)


def error(message, *args):
    info("Error: " + str(message), *args, format='*r', stream=sys.stderr)


def warn(message, *args):
    info("Warning: " + str(message), *args, format='*Y', stream=sys.stderr)


def die(message, *args):
    error(message, *args)
    sys.exit(1)


def get_number(prompt, **kwargs):
    default = kwargs.get('default', None)
    abort = kwargs.get('abort', None)

    if default is not None and abort is not None:
        prompt += ' (default is %s, %s to abort) ' % (default, abort)
    elif default is not None:
        prompt += ' (default is %s) ' % default
    elif abort is not None:
        prompt += ' (%s to abort) ' % abort

    number = None
    while number is None:
        ans = raw_input(prompt)
        if ans == str(abort):
            return None

        if ans:
            try:
                number = int(ans)
                if number < 1:
                    msg("Please enter a valid number.")
                    number = None
            except ValueError:
                msg("Please enter a valid number.")
        elif default is not None:
            number = default
    return number


def hline(label=None, **kwargs):
    """Draw an optionally colored or labeled horizontal line.
       Options:

       char       Char to draw the line with.  Default '-'
       color      Color of the label.  Default is no color.
       max_width  Maximum width of the line.  Default is 64 chars.

       See tty.color for possible color formats.
    """
    char      = kwargs.get('char', '-')
    color     = kwargs.get('color', '')
    max_width = kwargs.get('max_width', 64)

    cols, rows = terminal_size()
    if not cols:
        cols = max_width
    else:
        cols -= 2
    cols = min(max_width, cols)

    label = str(label)
    prefix = char * 2 + " " + label + " "
    suffix = (cols - len(prefix)) * char

    out = StringIO()
    if color:
        prefix = char * 2 + " " + color + cescape(label) + "@. "
        cwrite(prefix, stream=out, color=True)
    else:
        out.write(prefix)
    out.write(suffix)

    print out.getvalue()


def terminal_size():
    """Gets the dimensions of the console: cols, rows."""
    def ioctl_GWINSZ(fd):
        try:
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
        except:
            return
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (os.environ.get('LINES', 25), os.environ.get('COLUMNS', 80))

    return int(cr[1]), int(cr[0])
