"""
cats: cat for sequnce data
"""
DOCLINES = __doc__.split("\n")

from setuptools import setup,find_packages

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering :: Bio-Informatics',
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
    install_requires=['biopython', 'bcbio-gff'],
	setup_requires=['pytest-runner'],
	tests_require=['pytest>=2.8'],
	include_package_data=True,
    license="BSD",
    long_description="\n".join(DOCLINES[2:]),
    maintainer="Keith Hughitt",
    maintainer_email="khughitt@umd.edu",
    name="cats",
    packages=find_packages(),
    package_data={'':['*.fasta', '*.gff3']},
    platforms=["Linux", "Solaris", "Mac OS-X", "Unix"],
    provides=['cats'],
    url="https://github.com/khughitt/cats",
    zip_safe=False,
    version="0.3",
    entry_points={
        'console_scripts': ['cats = cats.ui.cli:main']
    }
)
