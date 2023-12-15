from setuptools import setup, find_packages

setup(
    name='chordata_web',
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
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
    scripts=['chordata/bin/chordata_server.py', 'chordata/bin/chordata_tool.py']
)
