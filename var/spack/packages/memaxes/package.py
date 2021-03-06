from spack import *

class Memaxes(Package):
    """MemAxes is a visualizer for sampled memory trace data."""

    homepage = "https://github.com/scalability-llnl/MemAxes"

    version('0.5', '5874f3fda9fd2d313c0ff9684f915ab5',
            url='https://github.com/scalability-llnl/MemAxes/archive/v0.5.tar.gz')

    depends_on("cmake@2.8.9:")
    depends_on("qt@5:")

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            cmake('..', *std_cmake_args)
            make()
            make("install")

