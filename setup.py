from setuptools import setup


setup(
    name='jpeglitch',
    version='0.2',
    py_modules=['jpeglitch'],
    install_requires=[
        'Click',
        'Pillow',
    ],
    entry_points='''
        [console_scripts]
        jpglitch=jpglitch:cli
    ''',
)
