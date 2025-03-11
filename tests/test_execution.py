import pytest
from quantumlib.execution.dynamic_selector import measure_noise_level
from quantumlib.execution.backend_manager import choose_backend

def test_measure_noise_level():
    backend = choose_backend(ibm_priority=False)
    noise = measure_noise_level(backend)
    assert noise >= 0.0, "Noise level should be non-negative"
