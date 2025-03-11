#!/usr/bin/env python3
"""
test_all.py - Quick 'all-in-one' script to manually test key functionalities
of the quantumlib project:
  1) Circuits: QFT roundtrip, small Grover, VQC configurations, HHL
  2) Optimizers: Adam & SPSA on a toy cost function
  3) Execution: transpile + run a circuit on Aer
  4) CLI sanity check (optional)
"""

import sys
from qiskit.circuit import Measure

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
    from qiskit import QuantumCircuit, transpile
    from qiskit_aer import Aer
    from qiskit.quantum_info import Statevector
    from quantumlib.circuits.grover import build_grover_circuit, phase_flip_oracle
    try:
        num_qubits = 3
        oracle = phase_flip_oracle('101')
        grover_qc = build_grover_circuit(num_qubits, oracle, iterations=1)
        
        grover_qc_no_meas = QuantumCircuit(grover_qc.num_qubits)
        for instr in grover_qc.data:
            if not isinstance(instr.operation, Measure):
                grover_qc_no_meas._append(instr.operation, instr.qubits, instr.clbits)
        sv = Statevector.from_label('0' * num_qubits).evolve(grover_qc_no_meas)
        amp_101 = abs(sv.data[5])
        amp_010 = abs(sv.data[2])
        print(f"[DEBUG] Grover |101> amplitude: {amp_101:.3f}, |010> amplitude: {amp_010:.3f}")
        if amp_101 < 0.5:
            print("[DEBUG] Warning: |101> amplitude too low, should be > 0.5 after 1 iteration.")
        
        backend = Aer.get_backend("aer_simulator")
        qc_t = transpile(grover_qc, backend)
        job = backend.run(qc_t, shots=512)
        result = job.result()
        counts = result.get_counts()

        top_state = max(counts, key=counts.get)
        if top_state == '101':
            print("[PASS] Grover's algorithm test => found '101' as marked state.")
        else:
            print("[WARN] Grover result top state not '101', but", top_state, "Counts:", counts)
    except Exception as e:
        print("[ERROR] Grover test crashed:", e)

def test_hhl():
    from qiskit import transpile
    from qiskit_aer import Aer
    from quantumlib.circuits.hhl import hhl_circuit
    try:
        # Create HHL circuit for 4 qubits
        qc = hhl_circuit(4)

        # Use Aer simulator
        backend = Aer.get_backend("aer_simulator")
        qc_t = transpile(qc, backend, optimization_level=3)
        
        # Add measurement to ancilla (qubit 3) to check success
        qc_t.measure(3, 1)  # Measure ancilla into a second classical bit
        
        # Run the circuit
        job = backend.run(qc_t, shots=512)
        result = job.result()
        counts = result.get_counts()

        # Check solution register (qubit 1) and ancilla (qubit 3)
        # Format: 'ancilla_solution' (e.g., '10' means ancilla=1, solution=0)
        success_counts = {k: v for k, v in counts.items() if k[0] == '1'}  # Ancilla = 1 indicates success
        total_success = sum(success_counts.values())
        if total_success > 0:
            success_prob = total_success / 512
            print(f"[PASS] HHL test => Success probability: {success_prob:.3f}, Counts (ancilla=1): {success_counts}")
            # Check solution distribution (should approximate x = [0.5, 1])
            x0_count = sum(v for k, v in success_counts.items() if k[1] == '0')
            x1_count = sum(v for k, v in success_counts.items() if k[1] == '1')
            total = x0_count + x1_count
            if total > 0:
                print(f"[DEBUG] Solution distribution: P(x0)={x0_count/total:.3f}, P(x1)={x1_count/total:.3f}")
        else:
            print("[WARN] HHL test => No successful runs detected.")
    except Exception as e:
        print("[ERROR] HHL test crashed:", e)

def test_vqc():
    from qiskit import transpile
    from qiskit_aer import Aer
    from quantumlib.circuits.vqc import VQC
    import numpy as np
    try:
        vqc1 = VQC(num_qubits=3, num_layers=2)
        params1 = np.random.random(3 * 2)
        qc1 = vqc1.bind_parameters(params1)
        qc1.measure_all()

        vqc2 = VQC(num_qubits=3, num_layers=2, rotation_gate='Rz', 
                   entanglement_pattern='full', entanglement_in_last_layer=True)
        params2 = np.random.random(3 * 2)
        qc2 = vqc2.bind_parameters(params2)
        qc2.measure_all()

        custom_pattern = [(0, 1), (1, 2), (2, 0)]
        vqc3 = VQC(num_qubits=3, num_layers=2, rotation_gate='Rx', entanglement_pattern=custom_pattern)
        params3 = np.random.random(3 * 2)
        qc3 = vqc3.bind_parameters(params3)
        qc3.measure_all()

        backend = Aer.get_backend("aer_simulator")
        circuits = [qc1, qc2, qc3]
        labels = ["Default (Ry, chain)", "Full (Rz, entangled last)", "Custom (Rx, ring)"]
        
        for qc, label in zip(circuits, labels):
            qc_t = transpile(qc, backend)
            job = backend.run(qc_t, shots=512)
            result = job.result()
            counts = result.get_counts()
            if len(counts) > 0:
                print(f"[PASS] VQC {label} => executed successfully, got counts: {counts}")
            else:
                print(f"[FAIL] VQC {label} => empty counts??")
    except Exception as e:
        print("[ERROR] VQC test crashed:", e)

def test_adam_optimizer():
    import numpy as np
    from quantumlib.optimizers.classical_opt import AdamOptimizer
    try:
        cost_fn = lambda x: (x[0]-2)**2 + 1
        opt = AdamOptimizer(maxiter=200, lr=0.05)
        best_params, best_val = opt.run(cost_fn, [0.0])
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
        opt = SPSAOptimizer(maxiter=300, c=0.2, a=0.1)
        best_params, best_val = opt.run(cost_fn, [10.0])
        if best_val < 5:
            print("[PASS] SPSA optimizer test => cost under 5, better than starting ~169.")
        else:
            print(f"[FAIL] SPSA final cost={best_val}, expected < 5 for decent result.")
    except Exception as e:
        print("[ERROR] SPSA optimizer test crashed:", e)

def test_basic_execution():
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
    test_hhl()  # Updated HHL test
    test_vqc()
    test_adam_optimizer()
    test_spsa_optimizer()
    test_basic_execution()
    test_cli_script()

if __name__=="__main__":
    main()