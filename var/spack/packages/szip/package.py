from spack import *

class Szip(Package):
    """SZIP implements an extended Rice adaptive lossless compression algorithm
    for sample data. All users can freely use the SZIP software to decode/decompress
    data. Certain uses of the SZIP software for encoding/compression may require
    appropriate licensing. For further information regarding licensing, contact ICs,
    LLC, at Joe.Feeley@ics-rhbd.com. Also note that there are multiple compression
    products on the web with the name \"SZIP\". The SZIP here is the one that is
    supported via hdfgroup.org.
    """

    homepage = "http://www.compressconsult.com/szip/"
    url      = "http://www.hdfgroup.org/ftp/lib-external/szip/2.1/src/szip-2.1.tar.gz"
    list_url = "http://www.hdfgroup.org/ftp/lib-external/szip"
    list_detph = 2

    version('2.1', '902f831bcefb69c6b635374424acbead')

    variant('dyn', default=False, description='+=static+dynamc libs; ~=only static')
    variant('opt', default=True, description='+=optimized; ~=debug')

    variant('lic', default=False, description='+=license ignorant; ~=license aware')
    
    def install(self, spec, prefix):

        config_args = [
            "CC=%s" % self.compiler.cc,
            "--enable-static",
            "--prefix=%s" % prefix
        ]

        if '+dyn' in spec:
            config_args += ["--enable-shared"]
        else:
            config_args += ["--disable-shared"]
      
        if '~opt' in spec:
            config_args += ["CFLAGS=-g"]

        if '+lic' in spec:
            config_args += ["--disable-encoding"]

        configure(*config_args)

        make("install")
