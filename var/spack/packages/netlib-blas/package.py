from spack import *
import os


class NetlibBlas(Package):
    """Netlib reference BLAS"""
    homepage = "http://www.netlib.org/blas/"
    url      = "http://www.netlib.org/blas/blas-3.5.0.tgz"

    version('3.5.0', 'ca21ed426f347c6ec6b136a181e587e5')

    variant('fpic', default=False, description="Build with -fpic compiler option")

    # virtual dependency
    provides('blas')

    # Doesn't always build correctly in parallel
    parallel = False

    def install(self, spec, prefix):
        mf = FileFilter('make.inc')
        mf.filter('^FORTRAN.*', 'FORTRAN = %s'%self.compiler.fc)
        mf.filter('^LOADER.*',  'LOADER = %s'%self.compiler.fc)
        mf.filter('^PLAT.*',  'PLAT =')
        mf.filter('^OPTS.*', 'OPTS = -O3 -qfixed')

        make('all')

        # No install provided
        mkdirp(prefix.lib)
        install('blas.a', prefix.lib)

        # Blas virtual package should provide blas.a and libblas.a
        with working_dir(prefix.lib):
            symlink('blas.a', 'libblas.a')
