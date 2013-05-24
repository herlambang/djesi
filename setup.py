import os
from distutils.core import setup

README = open(os.path.join(os.path.dirname(__file__), 'README')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='djesi',
    version='0.1',
    packages=['djesi', 'djesi.templatetags','djesi.middleware',],
    license='BSD License',  # example license
    description='Simple django ESI application',
    long_description=README,
    url='http://github.com/herlambang/djesi',
    author='Heru Herlambang',
    author_email='heruherlambang@gmail.com',
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)