from setuptools import setup, find_packages

setup(
    name = "air-imdb",
    desciption = "air-imdb",
    version = "1.0.0",
    install_requires = [
        "Flask==0.10.1",
        "SQLAlchemy==1.0.8",
        "MySQL-python==1.2.5",
        "python-dateutil==2.4.2",
        "IMDbPY==5.0",
        "voidpp-python-tools==1.0.0",
    ],
    scripts = [
        'bin/air-imdb-update',
    ],
    packages = find_packages(),
)

