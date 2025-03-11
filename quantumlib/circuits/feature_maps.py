"""
Quantum feature maps for ML. E.g. simple angle encoding or ZZFeatureMap.
"""
from qiskit import QuantumCircuit
import numpy as np

class ZZFeatureMap:
    """
    A typical 2-local feature map that encodes data x in rotations and entanglement phases.
    """
    def __init__(self, num_qubits, reps=2):
        self.num_qubits = num_qubits
        self.reps = reps
    
    def construct_circuit(self, data):
        """
        data: list or np array of length 'num_qubits'
        """
        qc = QuantumCircuit(self.num_qubits)
        # for reps times, apply angle encoding plus entangling
        for _ in range(self.reps):
            # apply RY
            for i, x in enumerate(data):
                qc.ry(x, i)
            # entangle with ZZ phases
            for i in range(self.num_qubits-1):
                qc.cz(i, i+1)
        return qc

class SimpleAngleMap:
    """
    Encodes each feature as an Ry rotation, no entanglement.
    """
    def __init__(self, num_qubits):
        self.num_qubits = num_qubits
    
    def construct_circuit(self, data):
        qc = QuantumCircuit(self.num_qubits)
        for i, x in enumerate(data):
            qc.ry(x, i)
        return qc
