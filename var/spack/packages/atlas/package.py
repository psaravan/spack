from spack import *

class Atlas(Package):
    """The ATLAS (Automatically Tuned Linear Algebra Software) project
       is an ongoing research effort focusing on applying empirical
       techniques in order to provide portable performance. At
       present, it provides C and Fortran77 interfaces to a portably
       efficient BLAS implementation, as well as a few routines from
       LAPACK."""
    homepage = "http://math-atlas.sourceforge.net"
    url      = "http://sourceforge.net/projects/math-atlas/files/Stable/3.10.2/atlas3.10.2.tar.bz2/download"

    version('3.10.2', 'a4e21f343dec8f22e7415e339f09f6da')

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            configure = Executable('../configure')
            configure("--prefix=%s" % prefix)
            make()
            make("install")
