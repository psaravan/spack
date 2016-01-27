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

class Sundials(Package):
    """SUNDIALS (SUite of Nonlinear and DIfferential/ALgebraic equation Solvers)"""

    homepage = "http://computation.llnl.gov/casc/sundials/"
    url      = "https://pkgs.fedoraproject.org/repo/extras/sundials/sundials-2.6.2.tar.gz/md5/3deeb0ede9f514184c6bd83ecab77d95/sundials-2.6.2.tar.gz"
    list_url = "https://pkgs.fedoraproject.org/repo/extras/sundials"
    list_depth = 2

    version('2.6.2', '3deeb0ede9f514184c6bd83ecab77d95')

#    depends_on("mpi")

#!/bin/sh -x
#    -DLAPACK_LIBRARIES:STRING="$FMROOT/lapack/3.5.0/$FMARCH/lib/liblapack.a;$FMROOT/lapack/3.5.0/$FMARCH/lib/libtmglib.a;$FMROOT/blas/19Apr11/$FMARCH/lib/libblas.a" \
#FMROOT=/projects/FASTMath/ATPESC-2015/install/fm-2015
#FMARCH=powerpc64-bgq-linux-gcc-4.4
#cmake \
#    -Wno-dev \
#    -DBUILD_SHARED_LIBS:BOOL=OFF \
#    -DBUILD_STATIC_LIBS:BOOL=ON \
#    -DMPI_ENABLE:BOOL=ON \
#    -DFCMIX_ENABLE:BOOL=ON \
#    -DCXX_ENABLE:BOOL=ON \
#    -DMPI_MPICC:FILEPATH=/soft/compilers/wrappers/gcc/mpicc \
#    -DMPI_MPICXX:FILEPATH=/soft/compilers/wrappers/gcc/mpicxx \
#    -DMPI_MPIF77:FILEPATH=/soft/compilers/wrappers/gcc/mpif77 \
#    -DCMAKE_CXX_COMPILER:FILEPATH=/soft/compilers/wrappers/gcc/mpicxx \
#    -DCMAKE_C_COMPILER:FILEPATH=/soft/compilers/wrappers/gcc/mpicc \
#    -DCMAKE_Fortran_COMPILER:FILEPATH=/soft/compilers/wrappers/gcc/mpif77 \
#    -DCMAKE_INSTALL_PREFIX:PATH=$FMROOT/sundials/2.6.1/$FMARCH \
#    -DEXAMPLES_INSTALL_PATH:STRING=/projects/FASTMath/ATPESC-2015/examples/sundials \
#    -DLAPACK_FOUND:BOOL=TRUE \
#    -DLAPACK_ENABLE:BOOL=ON \
#    -DLAPACK_LIBRARIES:STRING=$FMROOT/lapack/3.5.0/$FMARCH/lib/liblapack.a\;$FMROOT/lapack/3.5.0/$FMARCH/lib/libtmglib.a\;$FMROOT/blas/19Apr11/$FMARCH/lib/libblas.a \
#    -DEXTRA_LINK_LIBS:STRING=-lgfortran\;-lm \
#    -DSUNDIALS_RT_LIBRARY:FILEPATH=/usr/lib64/librt.a \
#../.


    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
