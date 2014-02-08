
from setuptools import setup


setup(
    name="sphinx-me",
    version=__import__("sphinx_me").__version__,
    author="Stephen McDonald",
    author_email="stephen.mc@gmail.com",
    description="",
    long_description=open("README.rst").read(),
    license="BSD",
    url="http://github.com/stephenmcd/sphinx-me/",
    py_modules=["sphinx_me",],
    entry_points="""
        [console_scripts]
        sphinx-me=sphinx_me:install
    """,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Documentation",
        "Topic :: Software Development :: Documentation",
        "Topic :: Utilities",
    ]
)
