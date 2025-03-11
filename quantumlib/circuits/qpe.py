"""
Quantum Phase Estimation
"""
from qiskit import QuantumCircuit

def qpe_circuit(unitary, num_ancillas, num_target):
    """
    Build QPE circuit using 'unitary' on 'num_target' qubits, 
    with 'num_ancillas' qubits for phase readout.
    """
    qc = QuantumCircuit(num_ancillas + num_target, num_ancillas)
    # step 1: hadamard on ancillas
    for a in range(num_ancillas):
        qc.h(a)
    # step 2: controlled unitary 2^a times
    for a in range(num_ancillas):
        reps = 2**a
        for _ in range(reps):
            qc.compose(unitary, list(range(num_ancillas, num_ancillas+num_target)), inplace=True, front=False, control_qubits=[a])
    # step 3: inverse QFT on ancillas
    # build or import an inverse QFT
    # for brevity, skip or do a partial
    # measure ancillas
    for a in range(num_ancillas):
        qc.measure(a, a)
    return qc
