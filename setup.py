import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="tidytwitter",
    version="0.0.2",
    description="Delete your old tweets and favorites using the Twitter API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/williamsmj/tidytwitter",
    author="Mike Lee Williams",
    author_email="mike@mike.place",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="twitter",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=["tweepy", "click"],
    entry_points={
        "console_scripts": [
            "tidytwitter=tidytwitter.tidytwitter:cli",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/williamsmj/tidytwitter/issues",
        "Source": "https://github.com/williamsmj/tidytwitter",
    },
)
