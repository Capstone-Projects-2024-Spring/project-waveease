from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='WaveEase',
    version='0.1.0',
    packages=find_packages(),
    description='A brief description of the package',
    long_description_content_type="text/markdown",
    url='https://github.com/Capstone-Projects-2024-Spring/project-waveease',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    install_requires=required,
    dependency_links=['https://download.pytorch.org/whl/cu113'],
)