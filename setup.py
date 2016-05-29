from setuptools import setup

setup(
    name="orthrus",
    version="0.1",
    packages=["orthrus"],
    install_requires=["ldap3>=1.3.1"],
    description="WUVT authentication library",
    license="AGPL3",
    author="mutantmonkey",
    author_email="orthrus@mutantmonkey.mx",
    url="https://github.com/wuvt/orthrus"
)
