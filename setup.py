import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kgscraper",
    version="0.0.1",
    author="Karolis Gadeikis",
    author_email="kgadeikis93@gmail.com",
    description="Turing College 2.4 Capstone project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tiskutis/Capstone24Scraper.git",
    packages=setuptools.find_packages(),
    install_requires = [
        'atomicwrites==1.4.0',
        'attrs==20.3.0',
        'beautifulsoup4==4.9.3',
        'certifi==2020.12.5',
        'chardet==4.0.0',
        'colorama==0.4.4',
        'idna==2.10',
        'iniconfig==1.1.1',
        'lxml==4.6.2',
        'numpy==1.19.5',
        'packaging==20.8',
        'pandas==1.2.0',
        'pluggy==0.13.1',
        'py==1.10.0',
        'pyparsing==2.4.7',
        'pytest==6.2.1',
        'python-dateutil==2.8.1',
        'pytz==2020.5',
        'requests==2.25.1',
        'six==1.15.0',
        'soupsieve==2.1',
        'toml==0.10.2',
        'urllib3==1.26.2'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
