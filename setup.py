from setuptools import setup, find_packages

setup(
    name='chordata',
    version="0.1.0",
    author="James Hickman",
    author_email="james@rationalboxes.com",
    description="Next generation Python web server framework",
    packages=[
        "chordata",
        "chordata.bin",
        "chordata.implementations",
        "chordata.interfaces",
        "chordata.ldap",
        "chordata.util"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
    entry_points={
        'console_scripts': [
            "chordata_server = chordata.bin.server:handler",
            "chordata_tool = chordata.bin.chordata_tool:__main__"
        ]
    }
)
