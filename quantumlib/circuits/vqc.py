from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from typing import Union

class VQC:
    """Variational Quantum Circuit with customizable rotations and entanglement."""
    def __init__(self, num_qubits: int, num_layers: int, rotation_gate: str = 'Ry', 
                 entanglement_pattern: Union[str, list] = 'chain', entanglement_in_last_layer: bool = False):
        """
        Initialize the VQC with customizable options.
        
        Args:
            num_qubits (int): Number of qubits in the circuit.
            num_layers (int): Number of layers in the circuit.
            rotation_gate (str): Type of rotation gate ('Ry', 'Rz', 'Rx'). Defaults to 'Ry'.
            entanglement_pattern (Union[str, list]): Entanglement structure ('chain', 'full', or list of (control, target) pairs).
                                                    Defaults to 'chain'.
            entanglement_in_last_layer (bool): Whether to include entanglement in the last layer. Defaults to False.
        """
        self.num_qubits = num_qubits
        self.num_layers = num_layers
        self.rotation_gate = rotation_gate.upper()
        self.entanglement_pattern = entanglement_pattern
        self.entanglement_in_last_layer = entanglement_in_last_layer
        
        # Validate rotation gate
        valid_gates = ['RY', 'RZ', 'RX']
        if self.rotation_gate not in valid_gates:
            raise ValueError(f"Rotation gate must be one of {valid_gates}")
        
        # Parameter vector for all rotation angles
        self.params = ParameterVector('θ', length=num_qubits * num_layers)
        
        # Build the quantum circuit
        self.circuit = QuantumCircuit(num_qubits)
        param_index = 0
        
        for layer in range(num_layers):
            # Rotation layer
            for q in range(num_qubits):
                if self.rotation_gate == 'RY':
                    self.circuit.ry(self.params[param_index], q)
                elif self.rotation_gate == 'RZ':
                    self.circuit.rz(self.params[param_index], q)
                elif self.rotation_gate == 'RX':
                    self.circuit.rx(self.params[param_index], q)
                param_index += 1
            
            # Entanglement layer (skip if last layer and entanglement_in_last_layer is False)
            if layer < num_layers - 1 or self.entanglement_in_last_layer:
                if self.entanglement_pattern == 'chain':
                    for q in range(num_qubits - 1):
                        self.circuit.cx(q, q + 1)
                elif self.entanglement_pattern == 'full':
                    for q1 in range(num_qubits):
                        for q2 in range(q1 + 1, num_qubits):
                            self.circuit.cx(q1, q2)
                elif isinstance(self.entanglement_pattern, list):
                    for control, target in self.entanglement_pattern:
                        if 0 <= control < num_qubits and 0 <= target < num_qubits:
                            self.circuit.cx(control, target)
                        else:
                            raise ValueError(f"Invalid qubit indices in entanglement pattern: ({control}, {target})")
                else:
                    raise ValueError("Entanglement pattern must be 'chain', 'full', or a list of (control, target) pairs")
    
    def bind_parameters(self, param_values: list) -> QuantumCircuit:
        """Bind a list of parameter values to the circuit and return a new QuantumCircuit."""
        if len(param_values) != len(self.params):
            raise ValueError("Parameter list length must equal number of circuit parameters.")
        bound_circuit = self.circuit.assign_parameters({self.params[i]: val 
                                                       for i, val in enumerate(param_values)})
        return bound_circuit