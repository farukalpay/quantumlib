class OptimizerBase:
    """
    Base class for an optimizer that can optimize a cost function
    with a certain parameter vector. 
    Each child must implement 'step' or 'run'.
    """
    def run(self, cost_fn, initial_params):
        """
        Perform the optimization. 
        returns (best_params, best_value)
        """
        raise NotImplementedError()
