"""
Construct a Grover circuit with user-specified oracle.
"""
from qiskit import QuantumCircuit

def build_grover_circuit(num_qubits, oracle: QuantumCircuit, iterations=1):
    """
    Builds a Grover circuit with 'iterations' of oracle+diffuser. 
    Oracle is a circuit that flips phase of the marked states.
    """
    qc = QuantumCircuit(num_qubits, num_qubits)
    # Initial superposition
    for q in range(num_qubits):
        qc.h(q)
    for _ in range(iterations):
        # Oracle
        qc.compose(oracle, range(num_qubits), inplace=True)
        # Diffusion
        diffusion(qc, num_qubits)
    qc.measure(range(num_qubits), range(num_qubits))
    return qc

def diffusion(qc, n):
    """
    Standard diffuser: H, X, multi-controlled Z, X, H
    """
    qc.barrier()
    for q in range(n):
        qc.h(q)
        qc.x(q)
    qc.h(n-1)
    qc.mcx(list(range(n-1)), n-1)  # multi-controlled X
    qc.h(n-1)
    for q in range(n):
        qc.x(q)
        qc.h(q)
    qc.barrier()
