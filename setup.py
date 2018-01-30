# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from aldryn_people import __version__

REQUIREMENTS = [
    'Django>=1.8,<2.0',
    'aldryn-boilerplates',
    'aldryn-common>=0.1.3',
    'aldryn-translation-tools>=0.1.0',
    'django-cms>=3.2',
    'django-parler>=1.4',
    'django-filer>=0.9.9',
    'djangocms-text-ckeditor',
    'easy-thumbnails',
    'phonenumbers',
    'six',

    # DO NOT REMOVE THE FOLLOWING, IT IS REQUIRED FOR EXISTING MIGRATIONS
    'django-phonenumber-field>=0.7.2,<2.0.0',
]

# https://pypi.python.org/pypi?%3Aaction=list_classifiers
CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Framework :: Django :: 1.8',
    'Framework :: Django :: 1.9',
    'Framework :: Django :: 1.10',
    'Framework :: Django :: 1.11',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
]

setup(
    name='aldryn-people',
    version=__version__,
    description='Aldryn People publishes profile pages for people in your '
                'organisation including team members, collaborators, '
                'partners, clients, and so on, including photographs and '
                'address information.',
    author='Divio AG',
    author_email='info@divio.ch',
    url='https://github.com/aldryn/aldryn-people',
    packages=find_packages(),
    license='LICENSE.txt',
    platforms=['OS Independent'],
    install_requires=REQUIREMENTS,
    classifiers=CLASSIFIERS,
    long_description=open('README.rst').read(),
    include_package_data=True,
    zip_safe=False,
    test_suite="test_settings.run",
)
