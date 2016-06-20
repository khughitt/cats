"""
cats: cat sequence
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
    description="Command-line tool for manipulating and displaying commonly used bioinformatic file formats.",
    install_requires=['biopython'],
	setup_requires=['pytest-runner'],
	tests_require=['pytest>=2.8'],
	include_package_data=True,
    license="BSD",
    maintainer="Keith Hughitt",
    maintainer_email="khughitt@umd.edu",
    name="cats",
    packages=find_packages(),
    package_data={'':['*.fasta', '*.gff3']},
    platforms=["Linux", "Solaris", "Mac OS-X", "Unix"],
    provides=['cats'],
    url="https://github.com/khughitt/cats",
    zip_safe=False,
    version="0.4",
    entry_points={
        'console_scripts': ['cats = cats.ui.cli:main']
    }
)
