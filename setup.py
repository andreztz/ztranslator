from setuptools import setup
from setuptools import find_packages


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="ztranslator",
    version="0.0.3",
    description="powerful command line translator.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    keywords="translator tradutor",
    author="André P. Santos",
    author_email="andreztz@gmail.com",
    url="https://github.com/andreztz/ztranslator",
    license="MIT",
    packages=find_packages(),
    install_requires=["requests"],
    entry_points={"console_scripts": ["ztranslator=translator.__main__:main"]},
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
    ],
)
