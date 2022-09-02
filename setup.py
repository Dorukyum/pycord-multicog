from setuptools import setup

classifiers = [
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
]

with open("README.md", encoding="utf-8") as f:
    readme = f.read()

setup(
    name="pycord-multicog",
    packages=["pycord.multicog"],
    version="1.0.0",
    license="MIT",
    description="A pycord extension that allows splitting command groups into multiple cogs",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Dorukyum",
    url="https://github.com/Dorukyum/pycord-multicog",
    keywords="Pycord",
    install_requires=["py-cord>=2.0.0"],
    classifiers=classifiers,
    project_urls={"Source": "https://github.com/Dorukyum/pycord-multicog"},
)
