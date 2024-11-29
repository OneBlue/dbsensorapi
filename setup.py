from setuptools import setup, find_packages

setup(
    name="dbsensorapi",
    version="1",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": ["dbsensorapi = dbsensorapi:main"]
        },
    install_requires=[
        'Flask>=0.12.2',
        'smbus2==0.5.0',
        'click==8.1.7'
        ]
    )

