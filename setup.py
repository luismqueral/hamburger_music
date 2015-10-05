from setuptools import setup

setup(
    name='HamburgerMusic',
    version='3.0.0',
    packages=['hamburger_music'],
    scripts=['scripts/makepoetry.py'],
    url="http://luisquer.al/hamburger-music",
    long_description=open('README.md').read(),
    install_requires=[
        "requests >= 2.0",
        "rauth >= 0.6",
        "pytumblr"
    ]
)
