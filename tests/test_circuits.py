import pytest
from qiskit.quantum_info import Statevector
from quantumlib.circuits import qft_circuit

def test_qft_back_and_forth():
    qc = qft_circuit(3)
    state_in = Statevector.from_label('101')
    after_qft = state_in.evolve(qc)
    after_inv = after_qft.evolve(qc.inverse())
    assert after_inv.equiv(state_in), "QFT + inverse QFT not returning original state"
