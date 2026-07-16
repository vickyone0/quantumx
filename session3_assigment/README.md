# Quantum Circuit Library

This assignment contains an interactive Python program for building and running a small library of important quantum circuits. The program creates a superposition circuit, a Bell state circuit, and a GHZ state circuit, then displays the circuit diagram, prints the statevector before measurement, runs the circuit on a Qiskit Aer simulator, and saves a histogram of the measurement results.

## Assignment Checklist

- Source code: `session3_assigment.py`
- Report: this `README.md`
- Output images: `qcl_output/superposition_histogram.png`, `qcl_output/bell_state_histogram.png`, and `qcl_output/ghz_state_histogram.png`

## Circuits Included

### Superposition

The superposition circuit applies a Hadamard gate to each qubit. For the default one-qubit circuit, this creates:

```text
(|0> + |1>) / sqrt(2)
```

When measured, the result should be close to 50% `0` and 50% `1`.

### Bell State

The Bell state circuit uses a Hadamard gate on the first qubit followed by a CNOT gate from qubit 0 to qubit 1. This creates the entangled state:

```text
(|00> + |11>) / sqrt(2)
```

Only `00` and `11` should appear in the measurement results, each with roughly equal probability.

### GHZ State

The GHZ circuit extends the Bell-state pattern across three qubits. It applies a Hadamard gate to qubit 0, then uses CNOT gates from qubit 0 to the remaining qubits. This creates:

```text
(|000> + |111>) / sqrt(2)
```

Only `000` and `111` should appear in the measurement results, each with roughly equal probability.

## Logic Behind the Implementation

1. `create_superposition()` builds a circuit with Hadamard gates.
2. `create_bell_state()` builds a two-qubit entangled Bell circuit.
3. `create_ghz_state()` builds a multi-qubit GHZ circuit.
4. `show_statevector()` prints the exact state before measurement.
5. `run_circuit()` copies the circuit, adds measurements, and executes it with `AerSimulator`.
6. `show_histogram()` prints shot counts and saves a histogram image to `qcl_output`.
7. The menu in `main()` lets the user run each demo repeatedly.

## How to Run

Install the required packages:

```bash
python3 -m pip install qiskit qiskit-aer matplotlib
```

Run the interactive program:

```bash
python3 session3_assigment.py
```

From the menu, choose:

```text
1. Superposition
2. Bell State
3. GHZ State
4. Exit
```

## Expected Output

Each selected circuit prints:

- A text circuit diagram
- The statevector before measurement
- Measurement counts from 1024 simulator shots
- A short explanation of the quantum behavior
- A saved histogram image in `qcl_output`

Because the simulator uses repeated shots, the exact counts can vary slightly each time. The probabilities should still be close to the theoretical 50/50 split for the valid outcomes.
