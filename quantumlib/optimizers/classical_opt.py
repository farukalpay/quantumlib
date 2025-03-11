import numpy as np
from .optimizer_base import OptimizerBase

class AdamOptimizer(OptimizerBase):
    def __init__(self, maxiter=100, lr=0.01, beta1=0.9, beta2=0.999, eps=1e-8):
        self.maxiter = maxiter
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.eps = eps
    
    def run(self, cost_fn, initial_params):
        params = np.array(initial_params, dtype=float)
        m = np.zeros_like(params)
        v = np.zeros_like(params)
        t = 0
        best_val = cost_fn(params)
        best_params = params.copy()
        for i in range(self.maxiter):
            t += 1
            grad = self._finite_diff_gradient(cost_fn, params)
            m = self.beta1*m + (1-self.beta1)*grad
            v = self.beta2*v + (1-self.beta2)*(grad**2)
            m_hat = m/(1 - self.beta1**t)
            v_hat = v/(1 - self.beta2**t)
            params = params - self.lr*(m_hat/(np.sqrt(v_hat)+self.eps))
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

class RMSPropOptimizer(OptimizerBase):
    def __init__(self, maxiter=100, lr=0.001, alpha=0.9, eps=1e-8):
        self.maxiter = maxiter
        self.lr = lr
        self.alpha = alpha
        self.eps = eps
    
    def run(self, cost_fn, initial_params):
        params = np.array(initial_params, dtype=float)
        Egrad2 = np.zeros_like(params)
        best_val = cost_fn(params)
        best_params = params.copy()
        for i in range(self.maxiter):
            grad = self._finite_diff_gradient(cost_fn, params)
            Egrad2 = self.alpha*Egrad2 + (1 - self.alpha)*(grad**2)
            params = params - (self.lr * grad)/(np.sqrt(Egrad2) + self.eps)
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
