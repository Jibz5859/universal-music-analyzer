from setuptools import setup, find_packages

setup(
    name="newproject",
    version="0.1.0",
    package_dir={"": "src"},  # Tells setuptools to look in src/
    packages=find_packages(where="src"),  # Finds all packages in src/
    install_requires=[
        'numpy>=1.21.0',
        'matplotlib>=3.5.0',
        'pillow>=9.0.0'
    ],
    python_requires=">=3.8",
    author="Your Name",
    description="Package for generating sine wave plots",
)