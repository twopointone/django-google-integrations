# Standard Library
import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = "0.0.1"

if sys.argv[-1] == "publish":
    try:
        import wheel

        print("Wheel version: ", wheel.__version__)
    except ImportError:
        print('Wheel library missing. Please run "pip install wheel"')
        sys.exit()
    os.system("python setup.py sdist upload")
    os.system("python setup.py bdist_wheel upload")
    sys.exit()


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="django-google-integrations",
    version=version,
    description="Integrate Google OAuth in your Django Rest-framework project",
    long_description=long_description,  # Long description read from the the readme file
    long_description_content_type="text/markdown",
    author="Primedigital Global",
    author_email="backend@primedigital.tech",
    url="https://github.com/PrimedigitalGlobal/django-google-integration",
    packages=[
        "django_google_integrations",
        "django_google_integrations/migrations",
    ],
    include_package_data=True,
    install_requires=[
        "google-api-python-client>2.8.0",
        "google-auth-httplib2>=0.0.4",
        "google-auth-oauthlib>0.4.0",
    ],
    license="MIT License",
    zip_safe=False,
    keywords="django rest_framework google signin",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 3.1",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
