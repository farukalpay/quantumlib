"""
HybridOptimizer: Dynamically chooses classical vs. quantum-native method 
based on backend performance (execution time, noise, etc.).
"""
import time
import numpy as np
from .optimizer_base import OptimizerBase
from .classical_opt import AdamOptimizer, RMSPropOptimizer
from .quantum_native_opt import SPSAOptimizer, QNGOptimizer

class HybridOptimizer(OptimizerBase):
    def __init__(self, maxiter=100, threshold_noise=0.01):
        """
        maxiter: total number of iterations
        threshold_noise: if measured noise/error rate above this => use quantum optimizer (SPSA).
        """
        self.maxiter = maxiter
        self.threshold_noise = threshold_noise
    
    def run(self, cost_fn, initial_params):
        # We'll maintain a current optimizer. We'll measure "noise" or "time" from cost_fn calls.
        # For demonstration, let's say if cost_fn(...) takes too long or we detect 'noise' => switch to SPSA.
        # If it's short => use Adam.
        # In practice, pass a 'backend_info' or measure variance. We'll do a simple time-based check.
        params = np.array(initial_params, dtype=float)
        best_val = cost_fn(params)
        best_params = params.copy()
        
        classical_opt = AdamOptimizer(maxiter=1, lr=0.01)  # run 1 iteration at a time
        quantum_opt = SPSAOptimizer(maxiter=1, c=0.1, a=0.01)
        
        current_opt = classical_opt  # start with classical
        for i in range(self.maxiter):
            start = time.time()
            # run 1 step of current optimizer
            local_best, local_val = current_opt.run(cost_fn, params)
            end = time.time()
            step_time = end - start
            
            # update
            params = local_best
            if local_val < best_val:
                best_val = local_val
                best_params = params.copy()
            
            # measure step_time as a proxy for 'backend performance'
            if step_time > 1.0:
                # if it's too big, switch to quantum approach
                current_opt = quantum_opt
            else:
                current_opt = classical_opt
        return best_params, best_val
