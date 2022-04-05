import os

from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='xcbv',
    version='0.2.0',
    description='CBVs so extra they can generate a menu',
    author='James Pic',
    author_email='jpic@yourlabs.org',
    url='http://xcbv.rtfd.org',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    long_description=read('README'),
    keywords='django views',
    entry_points = {
        'console_scripts': [
            'xcbv = xcbv_examples.manage:main',
        ],
    },
    requires=['six'],
    extras_require=dict(
        django=['django>=2.0'],
        demo=['django>=2.0'],
    ),
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
