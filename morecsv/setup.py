from setuptools import setup, find_packages

setup(
    name='morecsv',
    version='0.4.0',
    author='Unknownuserfrommars',
    author_email='unknownuserfrommars@protonmail.com',
    description='An enhanced CSV processing library with more features',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Unknownuserfrommars/morecsv',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    install_requires=[
        'pandas',
        'numpy',
        'matplotlib',
        'plotly'
    ],
)