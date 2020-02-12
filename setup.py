"""Setup for the IOTSocket package."""

import setuptools

with open('README.md') as f:
    README = f.read()

setuptools.setup(
    author="ABHIJITH BOPPE",
    author_email="abhijithas.eh@gmail.com",
    name='IOTSocket',
    license="MIT",
    description='IOTSocket is for IOT to make bidirectional full-duplex comunications securely from client and server side',
    version='v0.3',
    long_description=README,
    url='https://github.com/AbhijithAJ/IOT-Socket',
    packages=['IOTSocket'],
    python_requires=">=3.2",
    install_requires=['requests'],
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.8',
        'Topic :: IoT :: Server',
        'Topic :: IoT :: Client',
        'Intended Audience :: IOT Developers',
        'Intended Audience :: Backend Developers',
        'Operating System :: Linux',
    ],
)