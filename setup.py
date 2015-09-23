from setuptools import setup

setup(
    name='configm',
    version='0.1',
    author='Dan Kilman',
    author_email='dankilman@gmail.com',
    packages=['configm'],
    description='TBD',
    zip_safe=False,
    install_requires=[
        'argh',
        'sh',
        'path.py',
        'pyyaml'
    ],
    entry_points={
        'console_scripts': [
            'configm = configm.main:main',
        ],
    }
)
