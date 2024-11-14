# CircuitErrorFiltering
## Index
  - [Overview](#overview) 
  - [Setting](#setting)


## Overview
<!-- Write Overview about this project -->
- Circuit error filtering code filters the noisy result from the probability distribution with probability.


## Features
- The method only requires quantum circuit from qiskit and qubit register for error filtering.
- The error filtering only filters one qubit register (23.11.07)
- The error filtering only filters single qubit flip error (23.11.07)


### Basic Arguments
```
quantum_circuit: QuantumCircuit, EF_qreg: int, basis_gates = ['cx', 'id', 'rz', 'sx', 'x']
```

```SingleQubitBitFlip()``` creates new quantum circuit with error filtering.
NOTE: The given quantum circuit must exclude barrier and measurement.

```PostProcessing()``` process probability distribution from the errer filtered result.

### Work in progress
- Single arbitrary error filtering code
- More manual inputs
- Availablity to real quantum device
