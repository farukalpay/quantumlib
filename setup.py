# setup.py
import setuptools

setuptools.setup(
    name="quantumlib",
    version="0.1.0",
    author="Faruk Alpay",
    description="A modular quantum computing library for AerSimulator and IBM Quantum backends",
    packages=setuptools.find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "qiskit>=0.42.0",
        "qiskit-aer>=0.16.0",
        "numpy>=1.20.0",
        "scipy>=1.5.0",
        "matplotlib>=3.2",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            #IMPORTANT quantumlib/cli/run_circuit.py
            "run_circuit=quantumlib.cli.run_circuit:main",
        ],
    },
)
