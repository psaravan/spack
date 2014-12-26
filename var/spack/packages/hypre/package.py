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
from spack import *

class Hypre(Package):
    """The goal of the Scalable Linear Solvers project is to develop
       scalable algorithms and software for solving large, sparse
       linear systems of equations on parallel computers. The primary
       software product is hypre, a library of high performance
       preconditioners that features parallel multigrid methods for
       both structured and unstructured grid problems. The problems of
       interest arise in the simulation codes being developed at LLNL
       and elsewhere to study physical phenomena in the defense,
       environmental, energy, and biological sciences."""

    homepage = "https://computation.llnl.gov/project/linear_solvers/index.php"
    url      = "https://computation.llnl.gov/project/linear_solvers/download/hypre-2.9.0b.tar.gz"

    version('2.9.0b', '87bce8469240dc775c6c622c5f68fa87')
    version('2.8.0b', '6b4db576c68d2072e48efbc00ea58489')
    version('2.7.0b', '66ec0de71d93f68afc5c3a6742074bea')
    version('2.6.0b', '84381005bdddff69b62b43ca025070fd')

    depends_on("mpi")

    # 2.9.0b and above support CMake
    def install(self, spec, prefix):
        with working_dir("src/spack-build", create=True):
            cmake("..", *std_cmake_args)
            make()
            make("install")

    # Older versions of hypre must use configure
    @when("@:2.8.0b")
    def install(self, spec, prefix):
        with working_dir("src"):
            configure("--prefix=%s" % prefix)
            make()
            make("install")


