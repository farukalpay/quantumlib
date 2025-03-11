import argparse
import sys
from qiskit import transpile
from qiskit_aer import Aer
from quantumlib.execution.backend_manager import choose_backend
from quantumlib.circuits.grover import build_grover_circuit, phase_flip_oracle
from quantumlib.circuits.hhl import hhl_circuit
from quantumlib.circuits.vqc import VQC

def main():
    parser = argparse.ArgumentParser(description="Run a quantum circuit from quantumlib.")
    subparsers = parser.add_subparsers(dest="circuit", help="Circuit/algorithm to run", required=True)

    # Subparser for Grover
    grover_parser = subparsers.add_parser("grover", help="Run Grover's algorithm")
    grover_parser.add_argument("--num_qubits", type=int, required=True, help="Number of qubits for Grover's algorithm")
    grover_parser.add_argument("--marked_state", type=str, required=True, help="Marked state to search for (e.g., '101')")
    grover_parser.add_argument("--iterations", type=int, default=1, help="Number of Grover iterations")

    # Subparser for QAOA
    qaoa_parser = subparsers.add_parser("qaoa", help="Run QAOA algorithm")
    qaoa_parser.add_argument("--qubits", type=int, required=True, help="Number of qubits for QAOA")
    qaoa_parser.add_argument("--optimizer", type=str, default="spsa", choices=["spsa", "adam"], help="Optimizer for QAOA")

    # Subparser for HHL
    hhl_parser = subparsers.add_parser("hhl", help="Run HHL algorithm for linear systems")
    hhl_parser.add_argument("--num_qubits", type=int, default=4, help="Number of qubits (must be 4 for this HHL)")

    # Subparser for VQC
    vqc_parser = subparsers.add_parser("vqc", help="Run a Variational Quantum Circuit")
    vqc_parser.add_argument("--num_qubits", type=int, required=True, help="Number of qubits for VQC")
    vqc_parser.add_argument("--num_layers", type=int, default=2, help="Number of layers in VQC")
    vqc_parser.add_argument("--rotation_gate", type=str, default="Ry", choices=["Ry", "Rz", "Rx"], help="Rotation gate type")
    vqc_parser.add_argument("--entanglement_pattern", type=str, default="chain", help="Entanglement pattern (chain, full, or list)")

    # Common arguments
    parser.add_argument("--backend", type=str, default="auto", help="Which backend to use (auto, aer, ibmq_xxx, etc.)")
    parser.add_argument("--shots", type=int, default=1024, help="Number of shots for the simulation")

    args = parser.parse_args()

    # Build the circuit based on the selected algorithm
    if args.circuit == "grover":
        oracle = phase_flip_oracle(args.marked_state)
        qc = build_grover_circuit(args.num_qubits, oracle, iterations=args.iterations)
        print(f"Running Grover with num_qubits={args.num_qubits}, marked_state={args.marked_state}, iterations={args.iterations}")
    elif args.circuit == "qaoa":
        # Placeholder for QAOA: Using VQC as a simple substitute
        vqc = VQC(num_qubits=args.qubits, num_layers=2, rotation_gate="Ry", entanglement_pattern="chain")
        params = [0.1] * (args.qubits * 2)  # Dummy parameters
        qc = vqc.bind_parameters(params)
        qc.measure_all()
        print(f"Running QAOA with qubits={args.qubits}, optimizer={args.optimizer}")
    elif args.circuit == "hhl":
        qc = hhl_circuit(args.num_qubits)
        print(f"Running HHL with num_qubits={args.num_qubits}")
    elif args.circuit == "vqc":
        vqc = VQC(num_qubits=args.num_qubits, num_layers=args.num_layers, rotation_gate=args.rotation_gate,
                  entanglement_pattern=args.entanglement_pattern)
        params = [0.1] * (args.num_qubits * args.num_layers)  # Dummy parameters
        qc = vqc.bind_parameters(params)
        qc.measure_all()
        print(f"Running VQC with num_qubits={args.num_qubits}, layers={args.num_layers}, rotation={args.rotation_gate}, entanglement={args.entanglement_pattern}")
    else:
        print(f"Unsupported circuit: {args.circuit}. Supported options: grover, qaoa, hhl, vqc")
        sys.exit(1)

    # Decide on a backend
    if args.backend == "auto":
        backend = choose_backend(ibm_priority=False)
    elif args.backend.startswith("ibmq"):
        backend = Aer.get_backend("aer_simulator")  # Placeholder; update with IBMQ if available
    else:
        backend = Aer.get_backend("aer_simulator")

    # Run the circuit
    qc_t = transpile(qc, backend=backend)
    job = backend.run(qc_t, shots=args.shots)
    result = job.result()
    counts = result.get_counts()
    print("Circuit run successful. Measured counts:", counts)

if __name__ == "__main__":
    main()