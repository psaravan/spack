from spack import *

class Parmetis(Package):
    """ParMETIS is an MPI-based parallel library that implements a
       variety of algorithms for partitioning unstructured graphs,
       meshes, and for computing fill-reducing orderings of sparse
       matrices."""
    homepage = "http://glaros.dtc.umn.edu/gkhome/metis/parmetis/overview"
    url      = "http://glaros.dtc.umn.edu/gkhome/fetch/sw/parmetis/parmetis-4.0.3.tar.gz"

    version('4.0.3', 'f69c479586bf6bb7aff6a9bc0c739628')

#    depends_on('mpi')

    def install(self, spec, prefix):
        cmake(".",
              '-DGKLIB_PATH=%s/metis/GKlib' % pwd(),
              '-DMETIS_PATH=%s/metis' % pwd(),
              '-DCMAKE_C_COMPILER=%s' % self.compiler.cc,
              '-DCMAKE_CXX_COMPILER=%s' % self.compiler.cxx,
              '-DCMAKE_SKIP_RPATH=ON',
              '-DSHARED=0',
              *std_cmake_args)

        make()
        make("install")
