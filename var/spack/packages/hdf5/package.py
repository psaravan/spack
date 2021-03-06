from spack import *
import os

class Hdf5(Package):
    """HDF5 is a data model, library, and file format for storing and managing
       data. It supports an unlimited variety of datatypes, and is designed for
       flexible and efficient I/O and for high volume and complex data.
    """

    homepage = "http://www.hdfgroup.org/HDF5/"
    url      = "http://www.hdfgroup.org/ftp/HDF5/releases/hdf5-1.8.13/src/hdf5-1.8.13.tar.gz"
    list_url = "http://www.hdfgroup.org/ftp/HDF5/releases"
    list_depth = 3

    version('1.8.14', 'a482686e733514a51cde12d6fe5c5d95')
    version('1.8.13', 'c03426e9e77d7766944654280b467289')

    # global variants (eventually need to be handled across all packages)
    variant('dyn', default=False, description="+=static+dynamc libs; ~=only static")
    variant('opt', default=True, description="+=optimized; ~=debug")
    variant('langs', default=True, description="+=language API(s); ~=only default API")

    variant('reqdep', default=False, description='+=required dependent libs *only*; ~=See other xxxdep variants.')
    variant('stddep', default=True, description='+=standard/Common dependent libs; ~=See other xxxdep variants.')
    variant('alldep', default=False, description='+=all possible dependent libs; ~=See other xxxdep variants.')

    # package specific variants
    variant('mpiio', default=False, description="Enable MPI-IO support.")
    variant('zlib', default=True, description="Enable zlib compression features.")
    variant('szip', default=True, description="Enable SZip compression features.")

    # required dependencies
#    depends_on('mpi', when='+mpiio')
#    depends_on('mpi', when='+stddep')
#    depends_on('mpi', when='+alldep')

    # optional dependencies
    depends_on('zlib', when='+zlib')
    depends_on('zlib', when='+stddep')
    depends_on('zlib', when='+alldep')

    depends_on('szip', when='+szip')
    depends_on('szip', when='+stddep')
    depends_on('szip', when='+alldep')

    def install(self, spec, prefix):
        config_args = [
            "CC=%s" % self.compiler.cc,
            "--prefix=%s" % prefix,
            "--enable-static"
        ]

        if '+dyn' in spec:
            config_args += ["--enable-shared"]
        else:
            config_args += ["--disable-shared"]

        if '+opt' in spec:
            config_args += ["--enable-production"]
        else:
            config_args += ["--enable-debug=all", "--enable-trace", "--enable-using-memchecker"]

        if '+zlib' in spec or '+stddep' in spec or '+alldep' in spec:
            config_args += ["--with-zlib=%s" % spec['zlib'].prefix]

        if '+szip' in spec or '+stddep' in spec or '+alldep' in spec:
            config_args += ["--with-szlib=%s" % spec['szip'].prefix]

        if '+langs' in spec:
            config_args += ["--enable-hl"]
        else:
            config_args += ["--disable-hl"]

        # Note: use ~variant not -variant to test for negated variant in spec
	#
	# The compiler returned from Spack might contain the full compiler file path.
	# We only want the basename so derive it, if necessary.
	compiler_basename = os.path.basename(self.compiler.cc)
        if '+mpiio' in spec:
            config_args += ["--enable-parallel", "RUNPARALLEL=foo"]
        elif compiler_basename.startswith("mpi"):
            config_args += ["--enable-parallel", "RUNPARALLEL=foo"]

	if 'xl' in compiler_basename:
	    config_args += ["--enable-unsupported"]

        # Enable fortran interface if we have a fortran compiler and
        # fortran API isn't explicitly disabled
        if self.compiler.fc and '+langs' in spec:
            config_args += ["FC=%s" % self.compiler.fc,
                            "--enable-fortran",
                            "--enable-fortran2003"]

        # Enable C++ interface if we have a C++ compiler and
        # C++ API isn't explicitly disabled
        if self.compiler.cxx and '+langs' in spec:
            config_args += ["CXX=%s" % self.compiler.cxx,
                            "--enable-cxx"]

        configure(*config_args)

        make("install-recursive")

    def url_for_version(self, version):
        v = str(version)

        if version == Version("1.2.2"):
            return "http://www.hdfgroup.org/ftp/HDF5/releases/hdf5-" + v + ".tar.gz"
        elif version < Version("1.7"):
            return "http://www.hdfgroup.org/ftp/HDF5/releases/hdf5-" + version.up_to(2) + "/hdf5-" + v + ".tar.gz"
        else:
            return "http://www.hdfgroup.org/ftp/HDF5/releases/hdf5-" + v + "/src/hdf5-" + v + ".tar.gz"
