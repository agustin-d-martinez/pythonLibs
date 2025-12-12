from setuptools import setup, find_packages

setup(
    name='circuitanalisysToolkit',          
    version='0.1.0',
    description='FFT analysis, graphics utilities and symbolic tools',
    author='Agustin Damian Martinez',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
        'sympy',
        'matplotlib',
        'ipython',
    ],
    python_requires='>=3.8',
)
