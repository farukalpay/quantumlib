import pytest
import numpy as np
from quantumlib.optimizers.classical_opt import AdamOptimizer
from quantumlib.optimizers.quantum_native_opt import SPSAOptimizer

def test_adam_minimize_quadratic():
    cost_fn = lambda x: (x[0]-2)**2 + 1
    opt = AdamOptimizer(maxiter=50)
    best_params, best_val = opt.run(cost_fn, [0.0])
    assert abs(best_val-1) < 0.01, "Adam didn't converge near minimum"

def test_spsa_minimize_quadratic():
    cost_fn = lambda x: (x[0]+3)**2 + 2
    opt = SPSAOptimizer(maxiter=50, c=0.1, a=0.01)
    best_params, best_val = opt.run(cost_fn, [10.0])
    assert best_val<3, "SPSA expected to get near the minimum of 2 at x=-3"
