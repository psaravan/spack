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
import os
import sys
import string
import inspect
import glob
import imp

import llnl.util.tty as tty
from llnl.util.filesystem import join_path
from llnl.util.lang import memoized

import spack
import spack.error
import spack.spec
from spack.virtual import ProviderIndex

# Name of module under which packages are imported
_imported_packages_module = 'spack.packages'

# Name of the package file inside a package directory
_package_file_name = 'package.py'

# Valid package names can contain '-' but can't start with it.
valid_package_re = r'^\w[\w-]*$'

# Don't allow consecutive [_-] in package names
invalid_package_re = r'[_-][_-]+'


def valid_package_name(pkg_name):
    """Return whether the pkg_name is valid for use in Spack."""
    return (re.match(valid_package_re, pkg_name) and
            not re.search(invalid_package_re, pkg_name))


def validate_package_name(pkg_name):
    """Raise an exception if pkg_name is not valid."""
    if not valid_package_name(pkg_name):
        raise InvalidPackageNameError(pkg_name)


def class_name_for_package_name(pkg_name):
    """Get a name for the class the package file should contain.  Note that
       conflicts don't matter because the classes are in different modules.
    """
    validate_package_name(pkg_name)

    class_name = pkg_name.replace('_', '-')
    class_name = string.capwords(class_name, '-')
    class_name = class_name.replace('-', '')

    # If a class starts with a number, prefix it with Number_ to make it a valid
    # Python class name.
    if re.match(r'^[0-9]', class_name):
        class_name = "Num_%s" % class_name

    return class_name


def _autospec(function):
    """Decorator that automatically converts the argument of a single-arg
       function to a Spec."""
    def converter(self, spec_like):
        if not isinstance(spec_like, spack.spec.Spec):
            spec_like = spack.spec.Spec(spec_like)
        return function(self, spec_like)
    return converter


class PackageDB(object):
    def __init__(self, root):
        """Construct a new package database from a root directory."""
        self.root = root
        self.instances = {}
        self.provider_index = None


    @_autospec
    def get(self, spec):
        if spec.virtual:
            raise UnknownPackageError(spec.name)

        if not spec in self.instances:
            package_class = self.get_class_for_package_name(spec.name)
            self.instances[spec.name] = package_class(spec)

        return self.instances[spec.name]


    @_autospec
    def get_installed(self, spec):
        return [s for s in self.installed_package_specs() if s.satisfies(spec)]


    @_autospec
    def providers_for(self, vpkg_spec):
        if self.provider_index is None:
            self.provider_index = ProviderIndex(self.all_package_names())

        providers = self.provider_index.providers_for(vpkg_spec)
        if not providers:
            raise UnknownPackageError("No such virtual package: %s" % vpkg_spec)
        return providers


    def dirname_for_package_name(self, pkg_name):
        """Get the directory name for a particular package.  This is the
           directory that contains its package.py file."""
        return join_path(self.root, pkg_name)


    def filename_for_package_name(self, pkg_name):
        """Get the filename for the module we should load for a particular
           package.  Packages for a pacakge DB live in
           ``$root/<package_name>/package.py``

           This will return a proper package.py path even if the
           package doesn't exist yet, so callers will need to ensure
           the package exists before importing.
        """
        validate_package_name(pkg_name)
        pkg_dir = self.dirname_for_package_name(pkg_name)
        return join_path(pkg_dir, _package_file_name)


    def installed_package_specs(self):
        """Read installed package names straight from the install directory
           layout.
        """
        return spack.install_layout.all_specs()


    @memoized
    def all_package_names(self):
        """Generator function for all packages.  This looks for
           ``<pkg_name>/package.py`` files within the root direcotry"""
        all_package_names = []
        for pkg_name in os.listdir(self.root):
            pkg_dir  = join_path(self.root, pkg_name)
            pkg_file = join_path(pkg_dir, _package_file_name)
            if os.path.isfile(pkg_file):
                all_package_names.append(pkg_name)
            all_package_names.sort()
        return all_package_names


    def all_packages(self):
        for name in self.all_package_names():
            yield get(name)


    def exists(self, pkg_name):
        """Whether a package with the supplied name exists ."""
        return os.path.exists(self.filename_for_package_name(pkg_name))


    @memoized
    def get_class_for_package_name(self, pkg_name):
        """Get an instance of the class for a particular package.

           This method uses Python's ``imp`` package to load python
           source from a Spack package's ``package.py`` file.  A
           normal python import would only load each package once, but
           because we do this dynamically, the method needs to be
           memoized to ensure there is only ONE package class
           instance, per package, per database.
        """
        file_path = self.filename_for_package_name(pkg_name)

        if os.path.exists(file_path):
            if not os.path.isfile(file_path):
                tty.die("Something's wrong. '%s' is not a file!" % file_path)
            if not os.access(file_path, os.R_OK):
                tty.die("Cannot read '%s'!" % file_path)
        else:
            raise UnknownPackageError(pkg_name)

        class_name = class_name_for_package_name(pkg_name)
        try:
            module_name = _imported_packages_module + '.' + pkg_name
            module = imp.load_source(module_name, file_path)

        except ImportError, e:
            tty.die("Error while importing %s from %s:\n%s" % (
                pkg_name, file_path, e.message))

        cls = getattr(module, class_name)
        if not inspect.isclass(cls):
            tty.die("%s.%s is not a class" % (pkg_name, class_name))

        return cls


    def compute_dependents(self):
        """Reads in all package files and sets dependence information on
           Package objects in memory.
        """
        if not hasattr(compute_dependents, index):
            compute_dependents.index = {}

        for pkg in all_packages():
            if pkg._dependents is None:
                pkg._dependents = []

            for name, dep in pkg.dependencies.iteritems():
                dpkg = get(name)
                if dpkg._dependents is None:
                    dpkg._dependents = []
                dpkg._dependents.append(pkg.name)


    def graph_dependencies(self, out=sys.stdout):
        """Print out a graph of all the dependencies between package.
           Graph is in dot format."""
        out.write('digraph G {\n')
        out.write('  label = "Spack Dependencies"\n')
        out.write('  labelloc = "b"\n')
        out.write('  rankdir = "LR"\n')
        out.write('  ranksep = "5"\n')
        out.write('\n')

        def quote(string):
            return '"%s"' % string

        deps = []
        for pkg in all_packages():
            out.write('  %-30s [label="%s"]\n' % (quote(pkg.name), pkg.name))
            for dep_name, dep in pkg.dependencies.iteritems():
                deps.append((pkg.name, dep_name))
        out.write('\n')

        for pair in deps:
            out.write('  "%s" -> "%s"\n' % pair)
        out.write('}\n')


class InvalidPackageNameError(spack.error.SpackError):
    """Raised when we encounter a bad package name."""
    def __init__(self, name):
        super(InvalidPackageNameError, self).__init__(
            "Invalid package name: " + name)
        self.name = name


class UnknownPackageError(spack.error.SpackError):
    """Raised when we encounter a package spack doesn't have."""
    def __init__(self, name):
        super(UnknownPackageError, self).__init__("Package %s not found." % name)
        self.name = name