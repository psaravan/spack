from spack import *
import glob, os

class Netcdf(Package):
    """NetCDF is a set of software libraries and self-describing, machine-independent 
	data formats that support the creation, access, and sharing of array-oriented 
	scientific data."""

    homepage = "http://www.unidata.ucar.edu/software/netcdf/"
    url      = "ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-4.3.3.tar.gz"

    version('4.3.3', '5fbd0e108a54bd82cb5702a73f56d2ae')

    variant('dyn', default=False, description="+=static+dynamc libs; ~=static-only")
    variant('opt', default=True, description="+=optimized; ~=debug")

    variant('exo', default=True, description="+=exodus compatable; ~=default netcdf")

    # Specific Optional dependencies
    variant('hdf5', default=False, description="+=enable netcdf4; ~=disable netcdf-4")

    # Global short-hands for optional dependencies. These are mutually exclusive representing a
    # progression on dependencies from *only* required dependencies to all dependencies.
    variant('reqdep', default=False, description='+=required dependent libs *only*; ~=See other xxxdep variants.')
    variant('stddep', default=True, description='+=standard/Common dependent libs; ~=See other xxxdep variants.')
    variant('alldep', default=False, description='+=all possible dependent libs; ~=See other xxxdep variants.')

    # Dependencies:
    depends_on('hdf5', when='+hdf5')
    depends_on('hdf5', when='+stddep')
    depends_on('hdf5', when='+alldep')

    def install(self, spec, prefix):

        # if it hasn't been explicitly disabled, adjust netcdf header for ExodusII
        if '~exo' not in spec:
            mf = FileFilter('include/netcdf.h')
            mf.filter('^#define NC_MAX_DIMS\s*([0-9]*)\s*(.*)$',
                '#define NC_MAX_DIMS     65536 /* Was \\1; changed for ExodusII compatability */\n')
            mf.filter('^#define NC_MAX_VARS\s*([0-9]*)\s*(.*)$',
                '#define NC_MAX_VARS     524288 /* Was \\1; changed for ExodusII compatability */\n')
            mf.filter('^#define NC_MAX_VAR_DIMS\s*([0-9]*)\s*(.*)$',
                '#define NC_MAX_VAR_DIMS 8 /* Was \\1; changed for ExodusII compatability */\n')

        ldflags = []
        for dir in self.rpath:
            if dir == "%s/lib" % prefix or dir == "%s/lib64" % prefix:
                continue
            ldflags += ["-L%s" % dir]
            #ldflags += ["-lhdf5_hl_cpp", "-lhdf5_cpp", "-lhdf5hl_fortran", "-lhdf5_fortran", "-lhdf5_hl", "-lhdf5"]
	    parent_dir = os.path.dirname(dir)
	    current_lib_name = os.path.basename(parent_dir)
            if current_lib_name.startswith("hdf5"):
	    	ldflags += ["-lhdf5_hl_cpp", "-lhdf5_cpp", "-lhdf5hl_fortran", "-lhdf5_fortran", "-lhdf5_hl", "-lhdf5"]
		continue            

            for lib in glob.glob("%s/lib*.a" % dir):
                ldflags += ["-l%s" % os.path.basename(lib)[3:-2]]

        config_args = [
            "CC=%s" % self.compiler.cc,
            "--prefix=%s" % prefix,
            "--disable-dap",
            "--enable-static"]

        if '+hdf5' in spec or '+stddep' in spec or '+alldep' in spec:
            config_args += ["--enable-netcdf-4",
                            "CPPFLAGS=-I%s/include" % spec['hdf5'].prefix,
                            "LDFLAGS=%s" % ' '.join(ldflags)]
        else:
            config_args += ["--disable-netcdf-4"]

        if '+dyn' in spec:
            config_args += ["--enable-shared"]
        else:
            config_args += ["--disable-shared"]

        configure(*config_args)

        make("install")

	# Check the newly installed netcdf package. Currently disabled.
	# make("check")
