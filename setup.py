# TODO BROKEN FIXME
from setuptools import setup

version = "0.1"

setup(
    name='youtube-podcast-api',
    version=version,
    packages=['youtube_podcast_api'],
    include_package_data=True,
    license='GPLv3',
    author='Carlo De Pieri',
    description='A simple webservice that provides a rss feed from a YouTube channel.',
    scripts=[],
    install_requires=[
    ],
    extras_require={
        'dev': [
        ]
    }
)
