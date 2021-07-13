import io
from setuptools import find_packages, setup

# Read in the README for the long description on PyPI
def long_description():
  with io.open('../README.md', 'r', encoding='utf-8') as f:
    readme = f.read()
  return readme


setup(name='moamoa-crawler',
      version='0.1',
      description='crawl and alram',
      long_description=long_description(),
      url='https://github.com/jonggeun2001/jgkim-pp-crawl',
      author='jgkim',
      author_email='rla4509@naver.com',
      license='MIT',
      packages=find_packages(),
      classifiers=[
        'Programming Language :: Python :: 3.9',
      ],
      zip_safe=False)
