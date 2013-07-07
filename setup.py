from os.path import join, dirname
from setuptools import find_packages, setup


def get_install_requires():
    requirements = get_file_contents('pip-requires')
    install_requires = []
    for line in requirements.split('\n'):
        line = line.strip()
        if line and not line.startswith('-'):
            install_requires.append(line)
    return install_requires

def get_file_contents(filename):
    with open(join(dirname(__file__), filename)) as fp:
        return fp.read()

setup(name='hbase',
    version='0.1',
    description="A developer-friendly Python library to interact "
                  "with Apache HBase",
    long_description=get_file_contents('README.rst'),
    author="duanhongyi",
    author_email="duanhongyi@doopai.com",
    url='https://github.com/duanhongyi/hbase',
    install_requires=get_install_requires(),
    packages=find_packages(exclude=['tests']),
    license="MIT",
    classifiers=(
          "Development Status :: 4 - Beta",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python :: 2",
          "Topic :: Database",
          "Topic :: Software Development :: Libraries :: Python Modules",
    )
)
