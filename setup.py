from setuptools import setup, find_packages

setup(name='Discretizer',
      version='0.1',
      description='Discretization library for (D)BNs.',
      author='Daan Knoope',
      author_email='daan@knoope.dev',
      license='MIT',
      packages=find_packages(), install_requires=['pandas', 'numpy', 'mdlp-discretization'],
      python_requires='>3.6'
      )