from setuptools import setup, find_packages

setup(
    name='chordate',
    version="0.1.0",
    author="James Hickman",
    author_email="james@rationalboxes.com",
    description="Next generation Python web server framework",
    packages=[
        "chordate",
        "chordate.implementations",
        "chordate.interfaces",
        "chordate.ldap",
        "chordate.util"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
    entry_points={
        'console_scripts': [
            'chordate_server=chordate.bin.chordate_server:main',
            'chordate_tool=chordate.bin.chordate_tool:main'
        ]
    }
)
