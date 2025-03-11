"""
QAOA ansatz: alternates problem + mixer Hamiltonian for p layers.
"""
from qiskit import QuantumCircuit
from math import pi

class QAOAAnsatz:
    """
    QAOA ansatz builder:
     - problem hamiltonian as custom gates (Z, ZZ)
     - mixer as single-qubit X rotations
    """
    def __init__(self, num_qubits, p, problem_func, mixer_func=None):
        """
        num_qubits: number of qubits
        p: number of QAOA layers
        problem_func, mixer_func: callables that apply the problem/mixer unitaries
        """
        self.num_qubits = num_qubits
        self.p = p
        self.problem_func = problem_func
        self.mixer_func = mixer_func if mixer_func else self.default_mixer
    
    def default_mixer(self, qc, beta):
        """Apply standard X mixer: e^{-i * beta * sum X_i} ~ Rx(2*beta) on each qubit"""
        for q in range(self.num_qubits):
            qc.rx(2*beta, q)
    
    def build(self, params):
        """
        Build QAOA circuit with parameters: 
         params is expected to have length 2*p: [gamma_0, beta_0, gamma_1, beta_1, ..., gamma_{p-1}, beta_{p-1}]
        """
        qc = QuantumCircuit(self.num_qubits)
        # initial state = |+...+>
        for q in range(self.num_qubits):
            qc.h(q)
        
        # apply p layers
        idx = 0
        for layer in range(self.p):
            gamma = params[idx]
            beta = params[idx+1]
            idx += 2
            # problem layer
            self.problem_func(qc, gamma)
            # mixer layer
            self.mixer_func(qc, beta)
        return qc
