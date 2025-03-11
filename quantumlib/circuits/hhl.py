from qiskit import QuantumCircuit, ClassicalRegister
import numpy as np

def hhl_circuit(num_qubits):
    """
    Implements the HHL algorithm for solving linear systems A x = b, focused on a 2-dimensional system
    with A = [[2,0], [0,1]], b = [1, 1], using 4 qubits: input, solution, eigenvalue, ancilla.
    
    Args:
        num_qubits (int): Number of qubits, must be 4 for this implementation.
    
    Returns:
        QuantumCircuit: A quantum circuit implementing HHL steps: state preparation, QPE,
                       controlled rotations, uncomputing, and measurement.
    
    Raises:
        ValueError: If num_qubits is not 4, as this is a specific implementation.
    """
    if num_qubits != 4:
        raise ValueError("This implementation requires 4 qubits: input (b), solution (x), eigenvalue, ancilla")
    
    # Define circuit with 4 qubits and 2 classical bits
    qc = QuantumCircuit(4, 2)
    
    # Register assignments:
    # - Qubit 0: Input register (|b>)
    # - Qubit 1: Solution register (|x>)
    # - Qubit 2: Eigenvalue register (for QPE, 1 qubit for simplicity)
    # - Qubit 3: Ancilla register (for controlled rotations)
    
    # Step 1: State preparation
    # Prepare |b> in input register
    # Assuming b = [1,1], so |b> = (|0> + |1>) / sqrt(2)
    qc.h(0)  # Apply Hadamard to input register for superposition
    
    # Solution register starts as |0>
    # Eigenvalue register starts as H |0> for QPE
    qc.h(2)  # Hadamard on eigenvalue register
    
    # Ancilla register starts as |0>
    
    # Step 2: QPE for matrix A
    # For A = [[2,0], [0,1]], eigenvalues are 2 and 1
    # With 1-bit eigenvalue register, simplify by mapping:
    # Eigenvalue register |0> → λ=2, |1> → λ=1
    qc.x(2)  # Flip to control on |1> for λ=1
    qc.cz(2, 1)  # Controlled-Z on solution register for λ=1 (does nothing for scaling)
    qc.x(2)  # Unflip
    qc.cz(2, 1).c_if(0, 0)  # If eigenvalue register is 0 (λ=2), apply Z to solution
    
    # Step 3: Controlled rotation based on eigenvalue
    # Use ancilla to encode 1/λ scaling
    # For λ=2, scale by 1/2; for λ=1, scale by 1
    qc.cry(np.pi/2, 2, 3).c_if(0, 0)  # If eigenvalue register is 0, RY(π/2) for 1/sqrt(2)
    qc.cry(np.pi, 2, 3).c_if(0, 1)   # If eigenvalue register is 1, RY(π) for 1
    
    # Step 4: Uncompute QPE
    # Reverse the QPE operations
    qc.x(2)
    qc.cz(2, 1)
    qc.x(2)
    qc.cz(2, 1).c_if(0, 0)
    
    # Inverse Hadamard on eigenvalue register
    qc.h(2)
    
    # Step 5: Measure solution register and ancilla
    qc.measure(1, 0)  # Solution to classical bit 0
    qc.measure(3, 1)  # Ancilla to classical bit 1
    
    return qc