"""
Setup script for AION package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="aion",
    version="0.1.0",
    author="AION Team",
    description="AI-Oriented Notation - An AI-native intermediate representation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas>=1.3.0",
        "openai>=1.0.0",
        "anthropic>=0.7.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.8",
        ],
        "export": [
            "openpyxl>=3.0.0",
            "pyarrow>=10.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "aion=aion.cli:main",
        ],
    },
)
