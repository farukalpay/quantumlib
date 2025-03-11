#!/usr/bin/env python3
"""
test_all.py - Quick 'all-in-one' script to manually test key functionalities
of the quantumlib project:
  1) Circuits: QFT roundtrip, small Grover
  2) Optimizers: Adam & SPSA on a toy cost function
  3) Execution: transpile + run a circuit on Aer
  4) CLI sanity check (optional)
"""

import sys

def test_qft_roundtrip():
    from qiskit.quantum_info import Statevector
    from quantumlib.circuits.qft import qft_circuit
    try:
        qc = qft_circuit(3)
        sv_in = Statevector.from_label('101')
        sv_out = sv_in.evolve(qc).evolve(qc.inverse())
        if sv_out.equiv(sv_in):
            print("[PASS] QFT roundtrip test.")
        else:
            print("[FAIL] QFT roundtrip produced incorrect state.")
    except Exception as e:
        print("[ERROR] QFT roundtrip test crashed:", e)

def test_grover():
    """
    Build small Grover circuit, run on Aer simulator, expect top result '101'
    """
    from qiskit import QuantumCircuit, transpile
    from qiskit_aer import Aer  # IMPORTANT: from qiskit_aer, not from qiskit
    from quantumlib.circuits.grover import build_grover_circuit
    try:
        num_qubits = 3
        # sample oracle that flips phase of |101>
        oracle = QuantumCircuit(num_qubits)
        oracle.x(0)
        oracle.x(2)
        oracle.h(2)
        oracle.mcx([0,1], 2)
        oracle.h(2)
        oracle.x(0)
        oracle.x(2)

        grover_qc = build_grover_circuit(num_qubits, oracle, iterations=1)
        backend = Aer.get_backend("aer_simulator")
        qc_t = transpile(grover_qc, backend)
        job = backend.run(qc_t, shots=512)
        result = job.result()
        counts = result.get_counts()

        # Expecting '101' as top state
        top_state = max(counts, key=counts.get)
        if top_state == '101':
            print("[PASS] Grover's algorithm test => found '101' as marked state.")
        else:
            print("[WARN] Grover result top state not '101', but", top_state)
    except Exception as e:
        print("[ERROR] Grover test crashed:", e)

def test_adam_optimizer():
    import numpy as np
    from quantumlib.optimizers.classical_opt import AdamOptimizer
    try:
        cost_fn = lambda x: (x[0]-2)**2 + 1
        opt = AdamOptimizer(maxiter=200, lr=0.05)
        best_params, best_val = opt.run(cost_fn, [0.0])
        # Minimum cost is 1 at x=2
        if abs(best_val-1) < 0.5:
            print("[PASS] Adam optimizer test => near optimum.")
        else:
            print(f"[FAIL] Adam final cost={best_val}, expected near 1.")
    except Exception as e:
        print("[ERROR] Adam optimizer test crashed:", e)

def test_spsa_optimizer():
    import numpy as np
    from quantumlib.optimizers.quantum_native_opt import SPSAOptimizer
    try:
        cost_fn = lambda x: (x[0]+3)**2 + 2
        # minimum cost=2 at x=-3
        opt = SPSAOptimizer(maxiter=300, c=0.2, a=0.1)
        best_params, best_val = opt.run(cost_fn, [10.0])
        if best_val < 5:
            print("[PASS] SPSA optimizer test => cost under 5, better than starting ~169.")
        else:
            print(f"[FAIL] SPSA final cost={best_val}, expected < 5 for decent result.")
    except Exception as e:
        print("[ERROR] SPSA optimizer test crashed:", e)

def test_basic_execution():
    """
    Test a minimal circuit with transpile+run on Aer, ensuring no errors in logic.
    """
    from qiskit import QuantumCircuit, transpile
    from qiskit_aer import Aer
    try:
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0,1)
        qc.measure_all()

        backend = Aer.get_backend("aer_simulator")
        qc_t = transpile(qc, backend)
        job = backend.run(qc_t, shots=512)
        res = job.result()
        counts = res.get_counts()
        if len(counts) > 0:
            print("[PASS] Basic transpile+run => got counts:", counts)
        else:
            print("[FAIL] Basic transpile+run => empty counts??")
    except Exception as e:
        print("[ERROR] Basic execution test crashed:", e)

def test_cli_script():
    """
    Attempt 'run_circuit --help' if we have a console script installed.
    We'll skip if 'run_circuit' not found. We'll do a subprocess call.
    """
    import subprocess
    try:
        proc = subprocess.run(["run_circuit", "--help"], capture_output=True, text=True)
        if proc.returncode == 0:
            print("[PASS] CLI test => 'run_circuit --help' ran successfully.")
        else:
            print(f"[FAIL] CLI test => returncode={proc.returncode}.\n{proc.stderr}")
    except FileNotFoundError:
        print("[SKIP] CLI test => 'run_circuit' not found in PATH.")
    except Exception as e:
        print("[ERROR] CLI test crashed:", e)

def main():
    print("=== Testing quantumlib Manually ===")
    test_qft_roundtrip()
    test_grover()
    test_adam_optimizer()
    test_spsa_optimizer()
    test_basic_execution()
    test_cli_script()

if __name__=="__main__":
    main()