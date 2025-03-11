# circuits/vqc.py
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector

class VQC:
    """Variational Quantum Circuit with layered rotations and entanglement."""
    def __init__(self, num_qubits: int, num_layers: int):
        self.num_qubits = num_qubits
        self.num_layers = num_layers
        # Parameter vector for all rotation angles
        self.params = ParameterVector('θ', length=num_qubits * num_layers)
        # Build the quantum circuit
        self.circuit = QuantumCircuit(num_qubits)
        param_index = 0
        for layer in range(num_layers):
            # Rotation layer: apply Ry rotations on each qubit
            for q in range(num_qubits):
                self.circuit.ry(self.params[param_index], q)
                param_index += 1
            # Entanglement layer: chain of CNOTs (0->1, 1->2, ..., n-2->n-1)
            if layer < num_layers - 1:
                for q in range(num_qubits - 1):
                    self.circuit.cx(q, q+1)
    
    def bind_parameters(self, param_values: list) -> QuantumCircuit:
        """Bind a list of parameter values to the circuit and return a new QuantumCircuit."""
        if len(param_values) != len(self.params):
            raise ValueError("Parameter list length must equal number of circuit parameters.")
        bound_circuit = self.circuit.bind_parameters({self.params[i]: val 
                                                     for i, val in enumerate(param_values)})
        return bound_circuit