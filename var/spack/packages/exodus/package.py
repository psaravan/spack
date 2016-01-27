from spack import *
import os, glob

class Exodus(Package):
    """EXODUS II is a data model and file format developed to store and retrieve transient data for finite
       element analyses. It is used for preprocessing, postprocessing, as well as code to code data transfer.
       ExodusII is based on and uses netcdf. This exodus package includes the Nemesis parallel extensions.
    """

    homepage = "http://sourceforge.net/projects/exodusii"
    url      = "http://iweb.dl.sourceforge.net/project/exodusii/exodus-6.09.tar.gz"
    list_url = "http://sourceforge.net/projects/exodusii/files"
    list_depth = 1

    version('6.09', '2c139fc98706a04778d5607ab80b5d4d')
    version('6.06', 'cfd240dbc1251b08fb1d0ee2de40a44c')
    version('6.05', 'd46188f65012083483b4ad48c339e73b')
    version('5.26-1', 'f9b9c0c563f8ada2fc14ce14abe79dae')

    variant('dyn', default=False, description="Build both static and dynamic libs.")
    variant('opt', default=True, description="Build optimized with no debug support.")

    # required dependencies
    depends_on('netcdf+exo')

    def install(self, spec, prefix):

        ldflags = []
        for dir in self.rpath:
            if dir == "%s/lib" % prefix or dir == "%s/lib64" % prefix:
                continue
            ldflags += ["-L%s" % dir]
            for lib in glob.glob("%s/lib*.a" % dir):
                ldflags += ["-l%s" % os.path.basename(lib)[3:-2]]

        using_hdf5 = False
        nc_settings = open('%s/lib/libnetcdf.settings' % spec['netcdf'].prefix,'r').readlines()
        for l in nc_settings:
            if l[0:8] == 'LDFLAGS:' and 'hdf5' in l:
                using_hdf5 = True
        
        with working_dir('exodus'):
            mf = FileFilter('Makefile.standalone')
            mf.filter('^NETCDF\s*=\s*(.*)$', 'NETCDF = %s'%spec['netcdf'].prefix)
            mf.filter('^LDFLAGS\s*=\s*(.*)$', 'LDFLAGS ?= %s' % ldflags)
            mf.filter('^CC\s*=\s*(.*)$', 'CC ?= %s' % self.compiler.cc)
            if self.compiler.fc:
                mf.filter('^FC\s*=\s*(.*)$', 'FC ?= %s' % self.compiler.fc)
          
            if using_hdf5:
                mf.filter('^USING_NETCDF4\s*=\s*(.*)$', 'USING_NETCDF4 = "YES"')
            else:
                mf.filter('^USING_NETCDF4\s*=\s*(.*)$', 'USING_NETCDF4 = "NO"')

            if not self.compiler.fc:
                mf.filter('^SUBDIRS = cbind/src forbind/src cbind/test forbind/test',
                          'SUBDIRS = cbind/src cbind/test')
                mf.filter('^all:: libexodus.a libexoIIv2for.a libexoIIv2for32.a',
                          'all:: libexodus.a')
                mf.filter('^test:: libexodus.a libexoIIv2for.a',
                          'test:: libexodus.a')

            make('-f', 'Makefile.standalone', parallel=False)

            mkdirp(prefix.lib)
            for f in glob.glob('libexo*.*'):
                install(f, prefix.lib)

            mkdirp(prefix.include)
            with working_dir('cbind/include'):
                for f in glob.glob('*.h'):
                    install(f, prefix.include)

            if self.compiler.fc:
                with working_dir('forbind/include'):
                    for f in glob.glob('*.inc'):
                        install(f, prefix.include)
