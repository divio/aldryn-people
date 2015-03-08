# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from aldryn_people import __version__

REQUIREMENTS = [
    'django-parler',
    'phonenumbers',
    'django-phonenumber-field>=0.7.2',  # only here as quick-fix because old migrations depend on this field
    'vobject',
    'django-filer',
    'aldryn-common>=0.1.1',
    'djangocms-text-ckeditor',
    'aldryn-boilerplates',
]

CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
]

setup(
    name='aldryn-people',
    version=__version__,
    description='Renders a list of people',
    author='Divio AG',
    author_email='info@divio.ch',
    url='https://github.com/aldryn/aldryn-people',
    packages=find_packages(),
    license='LICENSE.txt',
    platforms=['OS Independent'],
    install_requires=REQUIREMENTS,
    classifiers=CLASSIFIERS,
    include_package_data=True,
    zip_safe=False,
    test_suite='cms_helper.run',
)
