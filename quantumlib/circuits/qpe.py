"""
Quantum Phase Estimation
"""
from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT

def qpe_circuit(unitary, num_ancillas, num_target):
    """
    Build QPE circuit using 'unitary' on 'num_target' qubits, 
    with 'num_ancillas' qubits for phase readout.

    Args:
        unitary: QuantumCircuit or Gate representing the unitary operator.
        num_ancillas (int): Number of ancilla qubits for phase estimation.
        num_target (int): Number of target qubits for the unitary.
    Returns:
        QuantumCircuit: QPE circuit with measurements on ancillas.
    """
    # Validate inputs
    if num_ancillas < 1 or num_target < 1:
        raise ValueError("num_ancillas and num_target must be positive integers.")
    if isinstance(unitary, QuantumCircuit) and unitary.num_qubits != num_target:
        raise ValueError(f"Unitary must act on {num_target} qubits.")

    # Initialize circuit
    qc = QuantumCircuit(num_ancillas + num_target, num_ancillas)
    
    # Step 1: Hadamard on ancillas
    qc.h(range(num_ancillas))
    
    # Step 2: Controlled unitary applications
    if isinstance(unitary, QuantumCircuit):
        unitary_gate = unitary.to_gate()
    else:
        unitary_gate = unitary
    controlled_unitary = unitary_gate.control(1)
    
    for a in range(num_ancillas):
        reps = 2**a
        for _ in range(reps):
            qc.append(controlled_unitary, [a] + list(range(num_ancillas, num_ancillas + num_target)))
    
    # Step 3: Inverse QFT on ancillas
    qc.append(QFT(num_ancillas, inverse=True), range(num_ancillas))
    
    # Step 4: Measure ancillas
    qc.measure(range(num_ancillas), range(num_ancillas))
    
    return qc