import compattern
from distutils.core import setup

CLASSIFIERS = """\
Intended Audience :: Science/Research
Intended Audience :: Developers
License :: Public Domain
Programming Language :: Python
Programming Language :: Python :: 3
Topic :: Software Development
Operating System :: POSIX
Operating System :: Unix

"""

setup(
    name='comparison_pattern',
    description='Scripts for mining comparison patterns from text',
    version=compattern.__version__,
    author='Vlad Niculae',
    author_email='vlad@vene.ro',
    classifiers=[_f for _f in CLASSIFIERS.split('\n') if _f]
)
