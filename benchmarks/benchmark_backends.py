"""
Lightweight script that compares execution time on Aer vs. possible real hardware.
"""

from qiskit import Aer, execute
import time

def benchmark_circuit(circuit, backend_name="aer_simulator"):
    from qiskit import IBMQ
    if backend_name=="aer_simulator":
        backend = Aer.get_backend("aer_simulator")
    else:
        provider=IBMQ.get_provider()
        backend = provider.get_backend(backend_name)
    start=time.time()
    job=execute(circuit, backend, shots=1024)
    result=job.result()
    end=time.time()
    return end-start, result.get_counts()

def main():
    print("Benchmarking a sample circuit on Aer and (optional) IBM device.")
    # Build a small circuit
    from quantumlib.circuits import qft_circuit
    qc=qft_circuit(3)
    t_aer, cts_aer=benchmark_circuit(qc, "aer_simulator")
    print(f"Aer time: {t_aer:.4f}s")
    # If user wants to do IBM, they can pass the device name or put logic here.

if __name__=="__main__":
    main()
