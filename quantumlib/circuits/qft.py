from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT
from math import pi

def qft_circuit(num_qubits, do_swap=True):
    """
    Build a Quantum Fourier Transform circuit for num_qubits.

    Args:
        num_qubits (int): Number of qubits, must be positive.
        do_swap (bool): Whether to include final swap gates for bit order (default=True).

    Returns:
        QuantumCircuit: QFT circuit, optionally with swaps for little-endian output.

    Raises:
        ValueError: If num_qubits is not positive.
    """
    if num_qubits <= 0:
        raise ValueError("Number of qubits must be positive.")
    
    # For large circuits, suggest using Qiskit's optimized QFT
    if num_qubits > 10:
        print("Warning: For num_qubits > 10, consider using Qiskit’s QFT for optimized gate decomposition.")
        return QFT(num_qubits, approximation_degree=0, do_swaps=do_swap).to_circuit()
    
    qc = QuantumCircuit(num_qubits, name="QFT")
    
    # Step 1: Apply Hadamard to each qubit for initial superposition
    for i in range(num_qubits):
        qc.h(i)
    
    # Step 2: Apply controlled phase gates for each pair (j > i)
    for i in range(num_qubits):
        for j in range(i + 1, num_qubits):
            angle = pi / (2 ** (j - i))
            qc.cp(angle, j, i)  # Control on j, target on i
    
    # Step 3: Optional swap to adjust bit order (little-endian to big-endian)
    if do_swap:
        for i in range(num_qubits // 2):
            qc.swap(i, num_qubits - i - 1)
    
    return qc