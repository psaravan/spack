# FIXME:
# This is a template package file for Spack.  We've conveniently
# put "FIXME" labels next to all the things you'll want to change.
#
# Once you've edited all the FIXME's, delete this whole message,
# save this file, and test out your package like this:
#
#     spack install chombo
#
# You can always get back here to change things with:
#
#     spack edit chombo
#
# See the spack documentation for more information on building
# packages.
#
from spack import *

class Chombo(Package):
    """FIXME: put a proper description of your package here."""
    # FIXME: add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url      = "https://github.com/psaravan/spack/blob/master/chombo-3.2.tar.gz?raw=true"

    version('3.2', '29d6bf7df0122baa3ada679cc8a4ebe2')

    # FIXME: Add dependencies if this package requires them.
    # depends_on("foo")

    def install(self, spec, prefix):
	# Manually cd into the lib/mk dir.
	with working_dir("lib/mk"):
		

        # FIXME: Add logic to build and install here
	        make("all")
