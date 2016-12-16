from distutils.core import setup

setup(
    name="pymumble",
    description="Python3 version of pymumble, mumble librairy used for multiple uses like making mumble bot"
    version='0.3.0',
    author='Robert Hendrickx',
    author_email='rober@percu.be',
    maintainer='Azlux',
    maintainer_email='azlux@outlook.com',
    url='https://github.com/azlux/pymumble',
    license='GPLv3',
    packages=['pymumble_py3'],
    install_requires=[
        'opuslib>=1.1.0',
        'protobuf>=3.1.0'
    ],
    classifiers=['Development Status :: 3 - Alpha',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
                 'Programming Language :: Python :: 2.7']
)
