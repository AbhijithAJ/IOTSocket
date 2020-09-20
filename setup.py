"""Setup for the IOTSocket package."""

from setuptools import setup, Extension


with open('README.md') as f:
    README = f.read()
 
setup(
    author="ABHIJITH BOPPE",
    author_email="abhijithas.eh@gmail.com",
    name='IOTSocket',
    license="MIT",
    description='To make bidirectional full-duplex comunications securely for iot devices',
    version='v1.0',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/AbhijithAJ/IOTSocket',
    keywords=['iotsocket', 'websocket', 'IOT', 'bidirectional', 'full duplex',
              'iotclient', 'iotserver', 'multiple devices', 'persistent socket','live socket','ssl','secured','replay attacks'],
    download_url='https://github.com/AbhijithAJ/IOTSocket/archive/v1.0.tar.gz',
    packages=['IOTSocket'],
    install_requires=['clrprint'],
    python_requires=">=3.2",
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'Operating System :: Unix',
    ],
)
