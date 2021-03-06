from distutils.core import setup
from os.path import join

setup(
    name='mikePlotLib',
    version='2.0.0',
    author='Michael Imelfort',
    author_email='mike@mikeimelfort.com',
    packages=['mikeplotlib'],
    scripts=[],
    url='http://pypi.python.org/pypi/mikePlotLib/',
    license='GPLv3',
    description='mikePlotLib',
    long_description=open('README.md').read(),
    package_data={'mikeplotlib': ['Menlo-Regular.ttf']},
    install_requires=[],
)

