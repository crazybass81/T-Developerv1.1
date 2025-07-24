from setuptools import setup, find_packages

setup(
    name="tdev",
    version="1.1.0",
    description="T-Developer - Agent Orchestration Platform",
    author="T-Developer Team",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0",
        "pyyaml>=6.0",
        "boto3>=1.28.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.1.0",
            "pylint>=2.17.0",
            "black>=23.3.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "tdev=tdev.cli:main",
        ],
    },
    python_requires=">=3.8",
)