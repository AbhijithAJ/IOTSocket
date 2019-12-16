from distutils.core import setup

setup(
    name='IOTSocket',
    version='1.3',
    author='Abhijith Boppe',
    author_email='abhijithas.eh@gmail.com',
    packages=['IOTSocket'],
    url='https://github.com/AbhijithAJ/IOTSocket',
    description='It is a secured IOT persistant bidirectional communication socket server written in Python',
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux, Windows",
    ],
)
