# quantum_annealing.py

from qiskit import QuantumCircuit

def annealing_circuit(schedule_params, num_qubits=2):
    """
    Construct a Trotterized quantum annealing circuit.

    Args:
        schedule_params (list of tuples): 
            Each tuple is (s, dt), where s in [0,1] is the annealing parameter,
            and dt is the time step for that segment.
        num_qubits (int): 
            Number of qubits in the circuit (>= 2).

    Returns:
        QuantumCircuit: The constructed quantum circuit implementing one pass
                        of the annealing schedule.

    Notes:
    - This version uses the convention H_m = sum_k X_k, consistent with 
      Qiskit's QAOA approach. That means the mixer gates have a *positive* angle 
      (rx(2 * theta_m)).
    - If you want H_m = -sum_k X_k instead, just change the mixer gate to 
      rx(-2 * theta_m).
    - The code also includes initial state preparation with Hadamards, which is
      common in QAOA-like approaches (|+> initial state). 
    - For multi-qubit systems (num_qubits > 2), it applies rzz gates to each pair 
      of adjacent qubits (a simple "chain" problem Hamiltonian).
    """
    if num_qubits < 2:
        raise ValueError("The number of qubits must be at least 2.")

    # Create a quantum circuit with the specified number of qubits
    qc = QuantumCircuit(num_qubits)

    # Optional initial state preparation: put all qubits in the |+> state
    # for a uniform superposition (common in many QAOA-style algorithms).
    qc.h(range(num_qubits))

    # Loop over each (s, dt) pair in the schedule
    for s, dt in schedule_params:
        # The fraction of the time devoted to the mixer
        theta_m = (1 - s) * dt

        # First half-step of the problem Hamiltonian (H_p = sum of ZZ interactions on adjacent qubits)
        for qubit in range(num_qubits - 1):
            qc.rzz(s * dt, qubit, qubit + 1)

        # Apply the mixer Hamiltonian: H_m = sum_k X_k, so e^{-i (1-s) X_k dt} => rx(2 * theta_m, k)
        for k in range(num_qubits):
            qc.rx(2 * theta_m, k)

        # Second half-step of the problem Hamiltonian
        for qubit in range(num_qubits - 1):
            qc.rzz(s * dt, qubit, qubit + 1)

    return qc