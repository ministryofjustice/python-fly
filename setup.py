from setuptools import setup, find_packages

setup(
    name='python-fly',
    version='0.0.2',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='A python package to run concourse fly',
    long_description=open('README.rst').read(),
    install_requires=[
        'requests',
    ],
    tests_require=[
        'parameterized'
    ],
    include_package_data=True,
    url='https://github.com/ministryofjustice/python-fly',
    author='Josh Rowe',
    author_email='josh.rowe@digital.justice.gov.uk',
    classifiers=(
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ),
)
