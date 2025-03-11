"""
Multi-controlled gates and other entanglement patterns
"""
from qiskit import QuantumCircuit

def multi_controlled_cz(qc: QuantumCircuit, ctrls, target):
    """
    Apply a multi-controlled Z gate on 'target' qubit with 'ctrls' as control qubits.
    Uses Qiskit's built-in MCX with 'z' phase approach or a decomposition.
    """
    # Qiskit supports mcx for X, but for CZ we do a trick or build a custom decomposition:
    # For brevity, let's do a naive approach: use MCX on an ancilla, then phase flip
    # or we can convert CZ to X-based controls. We'll do a simple approach if Qiskit version >= 0.30:
    qc.h(target)
    qc.mcx(ctrls, target) # multi-controlled X
    qc.h(target)
    # Now we have a multi-controlled Z. This is naive, can be improved.
