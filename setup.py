from setuptools import find_packages, setup

requires = [
    'flask'
    ]

setup(
    name='searchapp',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires
)
