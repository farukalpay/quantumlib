"""
Tracks or measures 'noise' or performance levels to guide dynamic selection of optimizers.
"""
def measure_noise_level(backend):
    """
    For demonstration, read out average gate error from backend.properties()
    or just return a placeholder.
    """
    props = None
    noise = 0.0
    try:
        props = backend.properties()
    except:
        return noise
    if props:
        # e.g. average CNOT error
        cnot_errs = []
        for gate in props.gates:
            if gate.gate == 'cx':
                for param in gate.parameters:
                    if param.name == 'gate_error':
                        cnot_errs.append(param.value)
        if cnot_errs:
            noise = sum(cnot_errs)/len(cnot_errs)
    return noise
