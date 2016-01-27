from spack import *

class Mfem(Package):
    """MFEM is a modular parallel C++ library for finite element methods. Its goal is
       to enable research and development of scalable finite element discretization
       and solver algorithms through general abstractions, accurate and
       flexible visualization, and tight integration with the hypre solver library.
    """

    homepage = "http://mfem.org"
    url      = "https://raw.githubusercontent.com/mfem/releases/gh-pages/mfem-3.0.1.tgz"
    list_url = "https://raw.githubusercontent.com/mfem/releases/gh-pages"
    list_depth = 1

    version('3.0.1', '3ccfbdab31dfaed8a58868b16480c60e')

    # global variants (need to be handled consistently across all packages)
    variant('debug', default=False, description="Enable debugging")
    variant('static', default=False, description="Build static libs")
    variant('shared', default=True, description="Build shared libs")
    variant('mpipar', default=False, description="Enable MPI Parallelism")
    variant('fortran', default=True, description="Enable Fortran interfaces")

#Compiler options:
#   OPTIM_FLAGS - Options for optimized build
#   DEBUG_FLAGS - Options for debug build
#   CXXFLAGS    - If not set, defined based on the above optimized/debug flags
#   CPPFLAGS    - Additional compiler options

    # required dependencies
#    depends_on('mpi', when='+mpipar')
    depends_on('hypre')
    depends_on('metis', when='+mpipar')
    depends_on('lapack')
#    depends_on('mesquite')

    def install(self, spec, prefix):

        config_vars = ["config"]
        config_vars += ["PREFIX=%s"%prefix]
        config_vars += ["CXX=%s"%self.compiler.cxx]
        if self.compiler.cxx.startswith("mpi") and '~mpipar' not in spec:
            config_vars += ["MPICXX=%s"%self.compiler.cxx]
        config_vars += ["MFEM_USE_LAPACK=YES"]
        config_vars += ["MFEM_THREAD_SAFE=YES"]
        config_vars += ["VERBOSE=YES"]
        config_vars += ["MFEM_USE_MEMALLOC=YES"]
#        config_vars += ["MFEM_USE_MESQUITE=YES"]
        config_vars += ["HYPRE_OPT=-I%s/include"%spec['hypre'].prefix,
                        "HYPRE_LIB=\"-L%s/lib -lhypre\""%spec['hypre'].prefix]
        config_vars += ["LAPACK_OPT=-I%s/include"%spec['lapack'].prefix,
                        "LAPACK_LIB=\"-L%s/lib -llapack -lblas -lgfortran\""%spec['lapack'].prefix]
#        config_vars += ["MESQUITE_OPT=-I%s/include"%spec['mesquite'].prefix,
#                        "MESQUITE_LIB=\"-L%s/lib -lmesquite\""%spec['mesquite'].prefix]

        if '+mpipar' in spec:
            config_vars += ["MFEM_USE_MPI=YES"]
            config_vars += ["MFEM_USE_METIS_5=YES"]
            config_vars += ["METIS_OPT=-I%s/include"%spec['metis'].prefix,
                            "METIS_LIB=\"-L%s/lib -lmetis\""%spec['metis'].prefix]
        else:
            config_vars += ["MFEM_USE_MPI=NO"]

        if '+debug' in spec:
            config_vars += ["MFEM_DEBUG=YES"]
        else:
            config_vars += ["MFEM_DEBUG=NO"]
     
        make(*config_vars, parallel=False)

        if '+mpipar' in spec:
            if '+debug' in spec:
                make("pdebug")
            else:
                make("parallel")
        else:
            if '+debug' in spec:
                make("debug")
            else:
                make("serial")

        make_vars = ["install", "PREFIX=%s"%prefix]
        make(*make_vars)

    def url_for_version(self, version):
        v = str(version)
        return "https://raw.githubusercontent.com/mfem/releases/gh-pages/mfem-" + v + ".tgz"
