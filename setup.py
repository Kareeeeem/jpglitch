from setuptools import setup


setup(
    name='jpglitch',
    version='0.2',
    py_modules=['jpglitch'],
    install_requires=[
        'Click',
        'Pillow',
    ],
    entry_points='''
        [console_scripts]
        jpglitch=jpglitch:cli
    ''',
)
