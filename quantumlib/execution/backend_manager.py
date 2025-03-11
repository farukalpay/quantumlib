"""
Provides utilities to detect available hardware or simulators,
and choose a default backend.
"""
import qiskit
from qiskit_aer import Aer

def get_backend_info(backend):
    """
    Return some info about the backend, e.g. name, qubit count, error rates if real device
    """
    info = {
        'name': backend.name()
    }
    props = backend.properties() if hasattr(backend, 'properties') else None
    if props:
        info['n_qubits'] = props.qubits
    return info

def choose_backend(ibm_priority=True):
    """
    If user has IBMQ and wants hardware, pick an IBM device if available.
    Otherwise default to Aer simulator.
    """
    try:
        from qiskit import IBMQ
        if ibm_priority and IBMQ.active_account() is not None:
            provider = IBMQ.get_provider()
            backend = provider.get_backend('ibmq_qasm_simulator')
            return backend
    except:
        pass
    # fallback
    return Aer.get_backend('aer_simulator')
