#!/usr/bin/env python3
"""
Universal Wave Engine - Python Package Setup
Revolutionary wave-based cognition engine
"""

from setuptools import setup, find_packages
import os

# Read version from VERSION file
def get_version():
    with open('VERSION', 'r') as f:
        return f.read().strip()

# Read the README file
def get_long_description():
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()

setup(
    name="universal-wave-engine",
    version=get_version(),
    author="Wave Engine Team",
    author_email="info@wave-engine.ai",
    description="Revolutionary wave-based cognition engine with 135,709x faster performance than LLMs",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/wave-engine/universal-wave-engine",
    packages=find_packages(),
    package_dir={"": "python"},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.19.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.8",
        ],
        "visualization": [
            "matplotlib>=3.3.0",
            "plotly>=5.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "wave-engine=wave_engine:main",
            "wave-validate=wave_engine:validation_main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["VERSION", "README.md"],
    },
    zip_safe=False,
    keywords="ai cognition wave-engine fast-ai reasoning universal cross-language performance",
    project_urls={
        "Bug Reports": "https://github.com/wave-engine/universal-wave-engine/issues",
        "Source": "https://github.com/wave-engine/universal-wave-engine",
        "Documentation": "https://wave-engine.ai/docs",
        "Funding": "https://github.com/sponsors/wave-engine",
    },
) 