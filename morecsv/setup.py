from setuptools import setup, find_packages

setup(
    name='morecsv',
    version='0.1.0',
    author='Your Name',
    author_email='your_email@example.com',
    description='An enhanced CSV processing library',
    long_description=open('README.md').read(),
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
    ],
)