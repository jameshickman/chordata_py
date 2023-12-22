from setuptools import setup, find_packages

setup(
    name='chordataweb',
    version="0.1.0",
    author="James Hickman",
    author_email="james@rationalboxes.com",
    description="Next generation Python web server framework",
    packages=[
        "chordataweb",
        "chordataweb.implementations",
        "chordataweb.interfaces",
        "chordataweb.ldap",
        "chordataweb.util"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
    entry_points={
        'console_scripts': [
            'chordate_server=chordataweb.bin.chordate_server:main',
            'chordate_tool=chordataweb.bin.chordate_tool:main',
            'chordate_chron=chordataweb.bin.chordate_chron:main'
        ]
    }
)
