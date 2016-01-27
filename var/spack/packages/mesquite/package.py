from spack import *
import os, glob

class Mesquite(Package):
    """Mesquite (Mesh Quality Improvement Toolkit) is designed to provide a stand-alone, portable,
       comprehensive suite of mesh quality improvement algorithms and components that can be used
       to construct custom quality improvement algorithms. Mesquite provides a robust and effective
       mesh improvement toolkit that allows both meshing researchers application scientists to
       benefit from the latest developments in mesh quality control and improvement.
    """

    homepage = "https://software.sandia.gov/mesquite"
    url      = "https://software.sandia.gov/mesquite/mesquite-2.3.0.tar.gz"
    list_url = homepage
    list_depth = 1

    version('2.3.0', 'f64948b5210d5ccffaa9a2482447b322')

    variant('dyn', default=False, description="+=static+dynamc libs; ~=static-only")
    variant('opt', default=True, description="+=optimized; ~=debug")

    variant('exodus', default=True, description="Build with Exodus.")
    variant('mpi', default=True, description="Build with MPI support.")

    variant('reqdep', default=False, description='+=required dependent libs *only*; ~=See other xxxdep variants.')
    variant('stddep', default=True, description='+=standard/Common dependent libs; ~=See other xxxdep variants.')
    variant('alldep', default=False, description='+=all possible dependent libs; ~=See other xxxdep variants.')

    # required dependencies
#    depends_on('mpi', when="+mpi")
    depends_on('exodus', when="+exodus")
    depends_on('exodus', when="+alldep")

#  --enable-32bit          Force 32bit object code
#  --enable-64bit          Force 64bit object code

    def install(self, spec, prefix):

        mf = FileFilter('configure')
        mf.filter('exoIIv2c','exodus')

        config_args = [
            "CXX=c++",
            "--prefix=%s" % prefix
        ]

        ldflags = []
        for dir in self.rpath:
            if dir == "%s/lib" % prefix or dir == "%s/lib64" % prefix:
                continue
            ldflags += ["-L%s" % dir]
            for lib in glob.glob("%s/lib*.a" % dir):
                ldflags += ["-l%s" % os.path.basename(lib)[3:-2]]
        config_args += ["LDFLAGS=%s" % ' '.join(ldflags)]

        if '+exodus' in spec or '+alldep' in spec:
            config_args += ["--with-exodus=%s" % spec['exodus'].prefix]
#            config_args += ["--with-netcdf=%s" % spec['netcdf'].prefix]

        if '+opt' in spec:
            config_args += ["--enable-release"]
        else:
            config_args += ["--enable-debug"]

        # Build static only or static *and* shared
        config_args += ["--enable-static"]
        if '+dyn' in spec:
            config_args += ["--enable-shared"]
        else:
            config_args += ["--disable-shared"]

        # Note: use ~variant not -variant to test for negated variant in spec
#        if '+mpi' in spec:
#            config_args += ["--with-mpi=%s" % spec['mpi'].prefix]
        if self.compiler.cc.startswith("mpi") and '~mpi' not in spec:
            config_args += ["--with-mpi"]

        configure(*config_args)

        make("install")
