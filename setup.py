import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent
README = (HERE / 'README.md').read_text()

setup(
    name="filehelper",
    version="1.0.1",
    description="Helper functions to manage files",
    long_description=README,
    long_description_content_type='text/markdown',
    author="Jonathan Grizou, Graham Keenan",
    author_email='jonathan.grizou@gmail.com, graham.keenan@outlook.com',
    license="MIT",
    url="https://github.com/tyrannican/filetools",
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.6'
)
