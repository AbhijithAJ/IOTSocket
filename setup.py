"""Setup for the IOTSocket package."""

import setuptools

with open('README.md') as f:
    README = f.read()

setuptools.setup(
    author="ABHIJITH BOPPE",
    author_email="abhijithas.eh@gmail.com",
    name='IOTSocket',
    license="MIT",
    description='to make bidirectional full-duplex comunications securely for iot devices',
    version='v0.3.3',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/AbhijithAJ/IOTSocket',
    packages=setuptools.find_packages(),
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
