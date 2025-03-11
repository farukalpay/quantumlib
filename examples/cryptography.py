"""
Quantum cryptography example: random bits from qubits or a simple Grover-based approach.
"""
from qiskit import Aer, execute, QuantumCircuit

def main():
    # Simple random key generator: n qubits in superposition -> measure
    n=4
    qc=QuantumCircuit(n, n)
    for i in range(n):
        qc.h(i)
    qc.measure(range(n), range(n))
    backend=Aer.get_backend("aer_simulator")
    job=execute(qc, backend, shots=1)
    counts=job.result().get_counts()
    key=list(counts.keys())[0]
    print("Quantum random key:", key)

if __name__=="__main__":
    main()
