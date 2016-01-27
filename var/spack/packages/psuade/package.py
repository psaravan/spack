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
import glob, os

class Psuade(Package):
    """
    Problem Solving environment for Uncertainty Analysis and Design Exploration.
    A software toolkit to facilitate the UQ tasks. PSUADE has a rich set of tools
    for performing uncertainty analysis, global sensitivity analysis, design
    optimization, model calibration, etc. In particular, PSUADE supports a
    global sensitivity methodology for models with large number of parameters
    and complex constraints.
    """

    homepage = "https://computation.llnl.gov/casc/uncertainty_quantification"
    url      = "https://computation.llnl.gov/casc/uncertainty_quantification/download/PSUADE_v1.7.4a.tar.gz"

    version('1.7.4a', '0043c97a20f4e86e4d55b4593d43679c')

    patch('set_external_libs.patch', when='@1.7.4a')

    variant('dyn', default=False, description="+=static+dynamc libs; ~=static-only")
    variant('opt', default=True, description="+=optimized; ~=debug")

    # Dependencies:
    depends_on('blas')
    depends_on('lapack')
    depends_on('metis')

#    depends_on("mpi")

    def install(self, spec, prefix):

        blas_libs = glob.glob('%s/lib/lib*.a' % spec['blas'].prefix)
        lapack_libs = glob.glob('%s/lib/lib*.a' % spec['lapack'].prefix)
        metis_libs = glob.glob('%s/lib/lib*.a' % spec['metis'].prefix)

        cmake_args = [
            '-DUSE_BOBYQA:BOOL=ON',
            '-DUSE_MARS:BOOL=ON',
            '-DCMAKE_CXX_COMPILER:FILEPATH=%s' % self.compiler.cxx,
            '-DCMAKE_C_COMPILER:FILEPATH=%s' % self.compiler.cc,
            '-DCMAKE_Fortran_COMPILER:FILEPATH=%s' % self.compiler.fc,
            '-DPSUADE_USE_BLAS:STRING=%s' % ';'.join(blas_libs),
            '-DPSUADE_USE_LAPACK:STRING=%s' % ';'.join(lapack_libs)]
#            '-DPSUADE_USE_METIS:STRING=%s' % ';'.join(metis_libs)]

        if '+opt' in spec:
            cmake_args += ['-DCMAKE_BUILD_TYPE:STRING=Release',
                           '-DBUILD_TESTING:BOOL=OFF']
        else:
            cmake_args += ['-DCMAKE_BUILD_TYPE:STRING=Debug',
                           '-DBUILD_TESTING:BOOL=ON']

        if '+dyn' in spec:
            cmake_args += ['-DBUILD_SHARED:BOOL=ON']
        else:
            cmake_args += ['-DBUILD_SHARED:BOOL=OFF']

        if self.compiler.cc.startswith("mpi"):
            cmake_args += ['-DPARALLEL_BUILD:BOOL=ON']
        else:
            cmake_args += ['-DPARALLEL_BUILD:BOOL=OFF']

        cmake(*cmake_args)

        make('install', parallel=False)
