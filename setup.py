import setuptools

setuptools.setup(
    name="pymumble",
    version='0.0.1',
    author='Robert Hendrickx',
    author_email='rober@percu.be',
    maintainer='Antonin Auroy',
    maintainer_email='antonin.auroy@gmail.com',
    url='https://github.com/aauroy/pymumble',
    license='GPLv3',
    packages=['pymumble'],
    install_requires=[
        'opuslib>=1.1.0',
        'protobuf>=2.6.1'
    ],
    classifiers=['Development Status :: 3 - Alpha',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
                 'Programming Language :: Python :: 2.7']
)