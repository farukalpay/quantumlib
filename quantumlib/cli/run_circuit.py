import argparse
import sys
from qiskit import transpile
from qiskit_aer import Aer
from quantumlib.execution.backend_manager import choose_backend

def main():
    parser = argparse.ArgumentParser(description="Run a quantum circuit from quantumlib.")
    parser.add_argument("--circuit", type=str, help="Path or name of circuit to run")
    parser.add_argument("--backend", type=str, default="auto", help="Which backend to use (auto, aer, ibmq_xxx, etc.)")
    parser.add_argument("--optimizer", type=str, default="auto", help="Which optimizer (auto, spsa, adam, etc.)")
    parser.add_argument("--shots", type=int, default=1024)
    args = parser.parse_args()

    # For demonstration, if circuit ends with .py, we do a placeholder.
    if args.circuit and args.circuit.endswith(".py"):
        print(f"Running script {args.circuit} with backend={args.backend}, optimizer={args.optimizer}, shots={args.shots}")
        # If you want, you could run it directly or import runpy, etc.
        sys.exit(0)

    # Otherwise, let's do a quick example circuit, or we can just error out
    if not args.circuit:
        print("No circuit specified.")
        sys.exit(1)

    # Example: build a trivial circuit
    from qiskit import QuantumCircuit
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0,1)
    qc.measure_all()

    # Decide on a backend
    if args.backend == "auto":
        # Use our backend_manager logic
        backend = choose_backend(ibm_priority=False)
    elif args.backend.startswith("ibmq"):
        # Or you can do a partial approach. For demonstration, let's do Aer anyway.
        backend = Aer.get_backend("aer_simulator")
    else:
        # if "aer"
        backend = Aer.get_backend("aer_simulator")

    # Now we do the recommended flow: transpile + backend.run
    qc_t = transpile(qc, backend=backend)
    job = backend.run(qc_t, shots=args.shots)
    result = job.result()
    counts = result.get_counts()
    print("Circuit run successful. Measured counts:", counts)