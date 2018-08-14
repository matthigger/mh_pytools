from setuptools import setup

setup(name='mh_pytools',
      version='0.1',
      description='python utilities',
      url='https://github.com/matthigger/mh_pytools',
      author='matt higger',
      author_email='matt.higger@gmail.com',
      license='MIT',
      packages=['mh_pytools'],
      install_requires=[
          'tqdm', 
          'matplotlib',
      ],
      zip_safe=False)
