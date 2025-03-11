import numpy as np
from .optimizer_base import OptimizerBase

class SPSAOptimizer(OptimizerBase):
    def __init__(self, maxiter=100, c=0.1, a=0.01):
        """
        c => step size for parameter perturbation
        a => learning rate scale
        """
        self.maxiter = maxiter
        self.c = c
        self.a = a
    
    def run(self, cost_fn, initial_params):
        params = np.array(initial_params, dtype=float)
        best_val = cost_fn(params)
        best_params = params.copy()
        for k in range(1, self.maxiter+1):
            ck = self.c/(k**0.2)  # typical SPSA decay
            ak = self.a/(k**0.6) 
            delta = np.random.choice([-1,1], size=len(params))
            params_plus = params + ck*delta
            params_minus = params - ck*delta
            fplus = cost_fn(params_plus)
            fminus = cost_fn(params_minus)
            g = (fplus - fminus)/(2*ck*delta)
            params = params - ak*g
            val = cost_fn(params)
            if val < best_val:
                best_val = val
                best_params = params.copy()
        return best_params, best_val

class QNGOptimizer(OptimizerBase):
    """
    Approx Quantum Natural Gradient using partial metric evaluation or a derivative-based approach.
    Placeholder: real QNG would measure the Fubini-Study metric.
    """
    def __init__(self, maxiter=50):
        self.maxiter = maxiter
    
    def run(self, cost_fn, initial_params):
        params = np.array(initial_params, dtype=float)
        # For demonstration, let's do a naive approach: measure an approximate metric = identity
        # Then standard gradient descent. Real QNG would require extra circuit evaluations.
        best_val = cost_fn(params)
        best_params = params.copy()
        for i in range(self.maxiter):
            grad = self._finite_diff_gradient(cost_fn, params)
            # QNG step: (F^-1) * grad -> if F = I, it's just grad
            step = grad
            # scale step by some factor
            alpha = 0.05
            params = params - alpha*step
            val = cost_fn(params)
            if val < best_val:
                best_val = val
                best_params = params.copy()
        return best_params, best_val
    
    def _finite_diff_gradient(self, cost_fn, params, epsilon=1e-5):
        grad = np.zeros_like(params)
        for i in range(len(params)):
            orig = params[i]
            params[i] = orig + epsilon
            fplus = cost_fn(params)
            params[i] = orig - epsilon
            fminus = cost_fn(params)
            grad[i] = (fplus - fminus)/(2*epsilon)
            params[i] = orig
        return grad
