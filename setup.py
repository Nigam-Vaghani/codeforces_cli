from setuptools import setup, find_packages
setup(
    name = "codeforces_cli",
    version="0.1.0",
    packages=find_packages(),
    install_requires = [
        "typer",
        "rich",
        "requests",
        "beautifulsoup4",
        "cloudscraper",
    ]
    ,
    entry_points = {
        "console_scripts": [
            "cf_cli=codeforces_cli.main:app"
        ]
    }
)