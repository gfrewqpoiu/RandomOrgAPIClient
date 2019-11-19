from setuptools import setup

long_desc = "A **very** barebones Random.Org API client for the production API, so Version 2."

setup(
    name="RandomOrgAPIClient",
    python_requires=">=3.7",
    version="0.0.1a",
    url="https://github.com/gfrewqpoiu/RandomOrgAPIClient",
    license="The Unlicense",
    description="Random.Org API Client",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    author="Kevin Striek",
    author_email="Kevin.Striek@gmail.com",
    py_modules=["RandomOrgAPIClient"],
    install_requires=[
        "httpx>=0.7.7",
    ])