from setuptools import setup, find_packages

setup(
	name='modulationToolkit',
	version='0.1.0',
    description="A simple digital and analog modulation library",
	author='Agustin Martinez',
	packages=find_packages(),
    install_requires=[
        "numpy",
    ],
	python_requires=">=3.8",
	keywords=['modulation', 'digital-modulation', 'signal-processing', 'communications', 'qam', 'qpsk'],
    license='MIT',

)
