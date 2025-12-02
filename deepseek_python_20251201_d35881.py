from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="abraham-ai",
    version="1.0.0",
    author="Abraham-AI Community",
    author_email="community@abraham-ai.org",
    description="Jewish-Chinese Wisdom Fusion AI Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bitonpro/AIMININUNG",
    project_urls={
        "Bug Tracker": "https://github.com/bitonpro/AIMININUNG/issues",
        "Documentation": "https://abraham-ai.org/docs",
        "Source Code": "https://github.com/bitonpro/AIMININUNG",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=0.990.0",
        ],
        "web": [
            "fastapi>=0.85.0",
            "uvicorn>=0.18.0",
            "jinja2>=3.0.0",
        ],
        "cloud": [
            "alibabacloud-core>=2.0.0",
            "alibabacloud-ecs>=3.0.0",
            "boto3>=1.24.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "abraham-ai=main:main",
            "abraham-cli=src.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "abraham_ai": [
            "data/*.json",
            "configs/*.yaml",
            "configs/*.json",
        ],
    },
    keywords=[
        "ai",
        "artificial-intelligence",
        "wisdom",
        "jewish",
        "chinese",
        "philosophy",
        "nlp",
        "machine-learning",
    ],
)