
from distutils.core import setup
from Cython.Distutils.extension import Extension
from Cython.Distutils import build_ext

# we need compiler flags from llvm-config

import subprocess

# 'borrowed' from 2.7 subprocess.py
def check_output(*popenargs, **kwargs):
    process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
    output, unused_err = process.communicate()
    retcode = process.poll()
    if retcode:
        cmd = kwargs.get("args")
        if cmd is None:
            cmd = popenargs[0]
        raise CalledProcessError(retcode, cmd, output=output)
    return output

cxxflags = check_output (['llvm-config', '--cxxflags']).strip().split()
ldflags  = check_output (['llvm-config', '--ldflags']).strip().split()
linkargs = check_output (['llvm-config', '--libs', 'core', 'bitreader', 'jit', 'native', 'asmparser']).strip().split()
llvm_version = check_output(['llvm-config', '--version']).strip().split('.')

compile_time_env = {
    'LLVM_VERSION': (int(llvm_version[0]), int(llvm_version[1])),
}

ext = Extension (
    'lljit.lljit',
    ['lljit/lljit.pyx', 'lljit/llvm.pxd'],
    language='c++',
    extra_compile_args=cxxflags+['-fexceptions'],
    extra_link_args=ldflags+linkargs,
    cython_compile_time_env=compile_time_env,
)

setup (
    name             = 'lljit',
    version          = '0.1.1',
    description      = 'cython interface to LLVM Jit',
    author           = "Sam Rushing",
    packages         = ['lljit'],
    ext_modules      = [ext],
    install_requires = ['cython>=0.15'],
    url              = 'http://github.com/mkushnir/lljit/',
    download_url     = "http://github.com/mkushnir/lljit/tarball/master#egg=lljit-0.1",
    license          = 'Simplified BSD',
    cmdclass = {'build_ext': build_ext},
    )
