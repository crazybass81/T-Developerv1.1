from setuptools import setup, find_packages

setup(
    name="tdev",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click",
        "pyyaml",
    ],
    entry_points={
        "console_scripts": [
            "tdev=tdev.cli:main",
        ],
    },
)