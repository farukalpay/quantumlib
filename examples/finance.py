"""
Quantum finance example: small portfolio optimization with a variational approach.
"""

from qiskit import Aer
from quantumlib.optimizers.hybrid_optimizer import HybridOptimizer
from quantumlib.circuits.ansatz_qaoa import QAOAAnsatz

def main():
    # Example usage with QAOA
    # We'll define a trivial 2-asset problem: cost= -p1*asset1 - p2*asset2 + penalty*(p1*p2)
    # For demonstration only.
    def problem_func(qc, gamma):
        # apply some phases
        # e.g. use Z rotations to represent cost
        for i in range(qc.num_qubits):
            qc.rz(-gamma*5.0, i)  # assume asset = 5
        # etc.
    
    ansatz = QAOAAnsatz(num_qubits=2, p=1, problem_func=problem_func)
    # We'll define a cost function using Aer
    def cost_fn(params):
        circ = ansatz.build(params)
        # measure or use statevector approach
        return 0.0  # placeholder
    
    hybrid = HybridOptimizer(maxiter=10)
    best_params, best_val = hybrid.run(cost_fn, [0.1, 0.2])
    print("Best val:", best_val, "with params:", best_params)

if __name__=="__main__":
    main()
