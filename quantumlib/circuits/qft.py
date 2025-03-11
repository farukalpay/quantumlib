"""
Quantum Fourier Transform circuit
"""
from qiskit import QuantumCircuit
from math import pi

def qft_circuit(num_qubits):
    qc = QuantumCircuit(num_qubits, name="QFT")
    for i in range(num_qubits):
        qc.h(i)
        for j in range(i+1, num_qubits):
            angle = pi / (2**(j - i))
            qc.cp(angle, j, i)
    # optional swap
    for i in range(num_qubits//2):
        qc.swap(i, num_qubits - i - 1)
    return qc
