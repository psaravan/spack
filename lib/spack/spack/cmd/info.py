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
import re
import textwrap
from StringIO import StringIO
from llnl.util.tty.colify import *
import spack
import spack.fetch_strategy as fs

description = "Get detailed information on a particular package"

def setup_parser(subparser):
    subparser.add_argument('-r', '--rst', action='store_true',
                           help="List all packages in reStructured text, for docs.")
    subparser.add_argument('name', metavar="PACKAGE", nargs='?', help="name of packages to get info on")


def format_doc(pkg, **kwargs):
    """Wrap doc string at 72 characters and format nicely"""
    indent = kwargs.get('indent', 0)

    if not pkg.__doc__:
        return ""

    doc = re.sub(r'\s+', ' ', pkg.__doc__)
    lines = textwrap.wrap(doc, 72)
    results = StringIO()
    for line in lines:
        results.write((" " * indent) + line + "\n")
    return results.getvalue()


def github_url(pkg):
    """Link to a package file on github."""
    return ("https://github.com/scalability-llnl/spack/blob/master/var/spack/packages/%s/package.py" %
            pkg.name)


def rst_table(elts):
    """Print out a RST-style table."""
    cols = StringIO()
    ncol, widths = colify(elts, output=cols, tty=True)
    header = " ".join("=" * (w-1) for w in widths)
    return "%s\n%s%s" % (header, cols.getvalue(), header)


def info_rst():
    """Print out information on all packages in restructured text."""
    pkgs = sorted(spack.db.all_packages(), key=lambda s:s.name.lower())

    print "Package List"
    print "=================="

    print "This is a list of things you can install using Spack.  It is"
    print "automatically generated based on the packages in the latest Spack"
    print "release."
    print

    print "Spack currently has %d mainline packages:" % len(pkgs)
    print
    print rst_table("`%s`_" % p.name for p in pkgs)
    print
    print "-----"

    # Output some text for each package.
    for pkg in pkgs:
        print
        print ".. _%s:" % pkg.name
        print
        print pkg.name
        print "-" * len(pkg.name)
        print "Links"
        print "    * `Homepage <%s>`__" % pkg.homepage
        print "    * `%s/package.py <%s>`__" % (pkg.name, github_url(pkg))
        print
        if pkg.versions:
            print "Versions:"
            print "  " + ", ".join(str(v) for v in reversed(sorted(pkg.versions)))
        if pkg.dependencies:
            print "Dependencies"
            print "  " + ", ".join("`%s`_" % d if d != "mpi" else d
                                   for d in pkg.dependencies)
            print
        print "Description"
        print format_doc(pkg, indent=2)
        print
        print "-----"


def info_text(pkg):
    """Print out a plain text description of a package."""
    print "Package:   ", pkg.name
    print "Homepage:  ", pkg.homepage

    print
    print "Safe versions:  "

    if not pkg.versions:
        print("None.")
    else:
        maxlen = max(len(str(v)) for v in pkg.versions)
        fmt = "%%-%ss" % maxlen
        for v in reversed(sorted(pkg.versions)):
            f = fs.for_package_version(pkg, v)
            print "    " + (fmt % v) + "    " + str(f)

    print
    print "Dependencies:"
    if pkg.dependencies:
        colify(pkg.dependencies, indent=4)
    else:
        print "    None"

    print
    print "Virtual packages: "
    if pkg.provided:
        for spec, when in pkg.provided.items():
            print "    %s provides %s" % (when, spec)
    else:
        print "    None"

    print
    print "Description:"
    if pkg.__doc__:
        print format_doc(pkg, indent=4)
    else:
        print "    None"


def info(parser, args):
     if args.rst:
         info_rst()

     else:
         if not args.name:
             tty.die("You must supply a package name.")
         pkg = spack.db.get(args.name)
         info_text(pkg)
