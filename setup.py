from setuptools import setup, find_packages

setup(
    name='scrapertype_scrapername',
    version='1.0.0',
    packages=find_packages(),
    url='',
    license='',
    author='Thiago Silva',
    author_email='someemail@email.com',
    description='Some description.',
    setup_requires=['wheel'],
    install_requires=[
        "click>=8.1.2",
        "setuptools>=62.1.0",
        "requests>=2.27.1",
        "bs4>=0.0.1",
        "Shapely>=1.8.1.post1",
        "pymongo>=4.1.1",
        "pandas>=1.4.2",
        "fastparquet>=0.8.1",
        "pyarrow>=10.0.1",
        "scrapy>=2.8.0",

    ],
    entry_points={
        'console_scripts': [
            "execute-scraper=scrapertype_scrapername.main:main"
        ]
    },
    include_package_data=True

)
