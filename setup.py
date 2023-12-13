from setuptools import setup, find_packages

setup(
    name='chordata',
    version="0.1.0",
    author="James Hickman",
    author_email="james@jameshickman.net",
    description="Next generation Python web server framework",
    packages=find_packages("chordata"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: LGPL 2.1",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
