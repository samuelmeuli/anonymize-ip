import io
import os
import sys
from shutil import rmtree

from setuptools import Command, find_packages, setup

# Package metadata
NAME = "anonymizeip"
DESCRIPTION = "Python library for anonymizing IP addresses"
URL = "https://github.com/samuelmeuli/anonymize-ip"
EMAIL = "dev@samuelmeuli.com"
AUTHOR = "Samuel Meuli"
REQUIRES_PYTHON = ">=3.3.0"
VERSION = None

# Packages
REQUIRED = []
EXTRAS = {}


directory = os.path.abspath(os.path.dirname(__file__))

# Import README.md and use it as long_description
try:
    with io.open(os.path.join(directory, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load package's __version__.py module as dictionary
about = {}
if not VERSION:
    with open(os.path.join(directory, NAME, "__version__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION


class UploadCommand(Command):
    """Support setup.py upload"""

    description = "Build and publish package"
    user_options = []

    @staticmethod
    def status(s):
        """Print in bold"""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(directory, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system("{0} setup.py sdist bdist_wheel --universal".format(
            sys.executable))

        self.status("Uploading the package to PyPI via Twine…")
        os.system("twine upload dist/*")

        self.status("Pushing git tags…")
        os.system("git tag v{0}".format(about["__version__"]))
        os.system("git push --tags")

        sys.exit()


setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=('tests',)),
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy"
    ],
    cmdclass={
        "upload": UploadCommand
    }
)
