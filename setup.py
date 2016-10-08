from setuptools import setup, find_packages
import pygunshot

setup(
    name = "PyGunShot",
    version = pygunshot.__version__,
    packages = find_packages(),
    scripts = ['scripts/example.py'],
    
    url ='https://github.com/metu-sparg/pygunshot/',
    license = 'MIT License',
    author = 'Huseyin Hacihabiboglu',
    author_email = "husshho@gmail.com",
    description = "pygunshot is a set of functions to generate gunshot  sounds given the scene geometry and ballistic parameters. Note that the module only provides anechoic samples and appropriate reverberation effects need to be added.",
    keywords = "gunshot sound synthesis"
)