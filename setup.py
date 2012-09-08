"""
moref: more for FASTA files
"""
DOCLINES = __doc__.split("\n")

from setuptools import setup

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering :: Bio-Informatics'
    'Operating System :: Microsoft :: Windows',
    'Operating System :: POSIX',
    'Operating System :: Unix',
    'Operating System :: MacOS'
]

setup(
    author="Keith Hughitt",
    author_email="khughitt@umd.edu",
    classifiers=CLASSIFIERS,
    description=DOCLINES[0],
    install_requires=['distribute', 'biopython'],
    license="BSD",
    long_description="\n".join(DOCLINES[2:]),
    maintainer="khughitt@umd.edu",
    maintainer_email="khughitt@umd.edu",
    name="moref",
    platforms=["Windows", "Linux", "Solaris", "Mac OS-X", "Unix"],
    provides=['moref'],
    py_modules=['moref'],
    url="",
    use_2to3=True,
    version="0.1",
    entry_points={
        'console_scripts': ['moref = moref:main']
    }
)