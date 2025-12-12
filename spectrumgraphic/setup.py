from setuptools import setup, find_packages

setup(
	name='spectrumgraphic',
	version='0.1.0',
	description='A library for creating spectrum graphics',
	author='Agustin Martinez',
	packages=find_packages(),
	install_requires=[
		'numpy',
		'matplotlib',
	],
	python_requires=">=3.8",
)
