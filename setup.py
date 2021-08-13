from setuptools import setup, find_packages


setup(
    name='triangulation',
    version='1.0',
    description='simple geometric triangulation with simulator',
    author='Rodion Anisimov',
    author_email='rodion_anisimov@mail.ru',
    url='https://github.com/Fricodelco/triangulation.git',
    install_requires=[
        'numpy==1.17.5',
        'scipy==1.5.4',
        'matplotlib==3.1.2',
    ],
    py_modules=["main"],
    packages=['triangulation'],
    include_package_data=True,
    package_data={'triangulation': ['*.json']},
    entry_points={
        'console_scripts': [
            'triangulation-cli = main:main',
        ],
    }
)
