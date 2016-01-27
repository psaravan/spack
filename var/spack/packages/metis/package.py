from spack import *

class Metis(Package):
    """METIS is a set of serial programs for partitioning graphs,
       partitioning finite element meshes, and producing fill reducing
       orderings for sparse matrices. The algorithms implemented in
       METIS are based on the multilevel recursive-bisection,
       multilevel k-way, and multi-constraint partitioning schemes."""

    homepage = "http://glaros.dtc.umn.edu/gkhome/metis/metis/overview"
    url      = "http://glaros.dtc.umn.edu/gkhome/fetch/sw/metis/metis-5.1.0.tar.gz"

    version('5.1.0', '5465e67079419a69e0116de24fce58fe')

    patch('gcc_coptions.patch', when='@5.1.0')

    variant('dyn', default=False, description="+=static+dynamc libs; ~=static-only")
    variant('opt', default=True, description="+=optimized; ~=debug")

#    depends_on('mpi')

    def install(self, spec, prefix):

        make_args = ['cc=%s' % self.compiler.cc,
                     'prefix=%s' % prefix]

        if '+dyn' in spec:            
            make_args += ['shared=1']

        if '~opt' in spec:
            make_args += ['debug=1',
                          'gdb=1',
                          'assert=1',
                          'assert2=1']

        make('config', *make_args, parallel=False)

        make('install')
