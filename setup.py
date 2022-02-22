# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='copc_dem',  # Required
    version='0.0.1',  # Required
    description='COPC processing for Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/hobu/copc_dem',
    author='Howard Butler',
    author_email='howard@hobu.co',
    classifiers=[  \
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],

    packages=find_packages(),  # Required
    python_requires='>=3.8',

    install_requires=['pdal','dask', 'Shapely','dask', 'pyproj','distributed','scipy'],

    entry_points={  # Optional
        'console_scripts': [
            'copc_dem=copc_dem.__main__:main',
        ],
    },

)


