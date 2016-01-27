from spack import *
import socket
import os
from os.path import join as pjoin

class Scalscmart(Package):
    """
    ScalSCMART: Scalable Software for Computational Mathematics Adavanced Research Toolkit.
    A computational mathematics software platform for advanced research in multi-physics
    applications, uncertainty quantification and/or optimization methodologies.
    """

    homepage = "scalscmart.llnl.gov"

    version('0.9', 'eae6d0ea43b963847b5afb4131df0253')

    depends_on('hypre')
    depends_on('mfem')
    depends_on('psuade')
    depends_on('samrai')
    depends_on('sundials')

    def url_for_version(self, version):
        print __file__
        dummy_tar_path =  os.path.abspath(pjoin(os.path.split(__file__)[0]))
        dummy_tar_path = pjoin(dummy_tar_path,"scalscmart.tar.gz")
        url      = "file://" + dummy_tar_path
        return url

    def install(self, spec, prefix):
        dest_dir     = env["SPACK_DEBUG_LOG_DIR"]
        # TODO: better name (use sys-type and compiler name ?)
        print "cmake executable: %s" % cmake_exe
        cfg = open(pjoin(dest_dir,"%s.cmake" % socket.gethostname()),"w")
        cfg.close()        
