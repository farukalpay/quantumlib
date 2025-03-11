"""
Construct a Grover circuit with user-specified oracle.
"""
from qiskit import QuantumCircuit

def phase_flip_oracle(state_binary_str):
    """
    Creates an oracle that flips the phase of the specified target state.
    
    Args:
        state_binary_str (str): Binary string of the target state (e.g., '101').
                                Qubit 0 is the rightmost bit (least significant).
    Returns:
        QuantumCircuit: Oracle circuit that applies a phase flip to the target state.
    """
    n = len(state_binary_str)
    qc = QuantumCircuit(n)
    # Apply X to qubits where the target state has '0'
    zero_bits = [i for i, bit in enumerate(state_binary_str) if bit == '0']
    for bit in zero_bits:
        qc.x(bit)
    # Apply multi-controlled Z using H and MCX on the target qubit (last qubit)
    target = n - 1
    qc.h(target)
    controls = list(range(n - 1))  # All qubits except the target
    qc.mcx(controls, target)
    qc.h(target)
    # Uncompute X gates
    for bit in zero_bits:
        qc.x(bit)
    return qc

def build_grover_circuit(num_qubits, oracle: QuantumCircuit, iterations=1):
    """
    Builds a Grover circuit with 'iterations' of oracle+diffuser.
    
    Args:
        num_qubits (int): Number of qubits in the circuit.
        oracle (QuantumCircuit): Circuit that flips the phase of the marked states.
        iterations (int): Number of Grover iterations (default=1).
    Returns:
        QuantumCircuit: Complete Grover circuit with measurements.
    """
    qc = QuantumCircuit(num_qubits, num_qubits)
    # Initial superposition
    for q in range(num_qubits):
        qc.h(q)
    # Apply oracle and diffuser iterations
    for _ in range(iterations):
        qc.compose(oracle, range(num_qubits), inplace=True)
        diffusion(qc, num_qubits)
    qc.measure(range(num_qubits), range(num_qubits))
    return qc

def diffusion(qc, n):
    """
    Standard diffuser: H, X, multi-controlled Z, X, H.
    
    Args:
        qc (QuantumCircuit): Circuit to append the diffuser to.
        n (int): Number of qubits.
    """
    qc.barrier()
    for q in range(n):
        qc.h(q)
        qc.x(q)
    qc.h(n-1)
    qc.mcx(list(range(n-1)), n-1)  # Multi-controlled X
    qc.h(n-1)
    for q in range(n):
        qc.x(q)
        qc.h(q)
    qc.barrier()