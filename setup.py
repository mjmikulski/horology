from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='horology',
      version='1.0.0',
      author='Maciej J Mikulski',
      author_email='maciej.mikulski.jr@gmail.com',
      description='measure time conveniently',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/mjmikulski/horology',
      license='MIT',
      install_requires=[],
      python_requires='>=3.6',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Utilities',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Testing',
          'Topic :: Software Development :: Libraries :: Python Modules',
          "Operating System :: OS Independent",
      ],
      keywords='timing profiling measure time complexity duration optimization',
      packages=find_packages()
      )
