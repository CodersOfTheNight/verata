# -*- coding: UTF-8 -*-
from setuptools import setup
from pip.req import parse_requirements

from grazer.version import get_version

install_reqs = list(parse_requirements("requirements.txt", session={}))

setup(name="verata",
      version=get_version(),
      author="Šarūnas Navickas",
      author_email="zaibacu@gmail.com",
      url="https://github.com/CodersOfTheNight/verata",
      packages=["grazer", "grazer.core", "grazer.readers.local"],
      install_requires=[str(ir.req) for ir in install_reqs],
      test_suite="pytest",
      tests_require=["pytest"],
      setup_requires=["pytest-runner"],
      entry_points={"console_scripts": ["verata = grazer.run:main"]}
      )
