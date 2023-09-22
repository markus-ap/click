from setuptools import setup

name = "bouvet"

setup(
    name=name,
    version='0.0.1',
    py_modules=[name],
    install_requires=[
        'Click', 'requests'
    ],
    entry_points=f'''
        [console_scripts]
        {name}={name}:cli
    ''',
)