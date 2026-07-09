# Single-Qubit Gate Explorer

This repository contains a Python program for exploring how common single-qubit gates change a qubit state. The program builds a one-qubit quantum circuit, applies a selected gate, calculates the measurement probabilities, and visualizes the final state on a Bloch sphere.

## Assignment Checklist

- Source code: `session2_assigment.py`
- Report: this `README.md`
- Output images: `outputs/quantum_circuit.svg`, `outputs/bloch_sphere.svg`, and `outputs/measurement_probabilities.svg`
- Sample console output: `outputs/console_output.txt`

## Approach

The qubit starts in the computational basis state `|0>`. The user chooses one of five supported gates:

- `X`: flips `|0>` to `|1>`
- `Y`: flips the bit and adds a phase
- `Z`: changes the phase of `|1>`; when applied to `|0>`, the visible state remains `|0>`
- `H`: creates an equal superposition of `|0>` and `|1>`
- `RY(theta)`: rotates the qubit around the Bloch sphere's Y axis by a user-provided angle

After the selected gate is applied, Qiskit's `Statevector.from_instruction()` computes the final statevector. The program then uses the statevector probabilities to report the likelihood of measuring `|0>` or `|1>`.

## Logic Behind the Implementation

1. A dictionary maps menu choices to human-readable gate names.
2. `choose_gate()` validates interactive user input.
3. `build_circuit()` creates a `QuantumCircuit(1)` and applies the selected gate.
4. `get_probabilities()` converts the circuit to a statevector and returns the probabilities for `|0>` and `|1>`.
5. `plot_bloch_multivector()` draws the final qubit state on the Bloch sphere.
6. The optional command-line mode can save the quantum circuit, Bloch sphere, measurement probability chart, and console output into an output directory.

## How to Run

Install the dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Run the interactive program:

```bash
python3 session2_assigment.py
```

Generate output files without opening windows:

```bash
python3 session2_assigment.py --gate h --save-dir outputs --no-show
```

Generate an `RY` rotation example:

```bash
python3 session2_assigment.py --gate ry --theta 1.5708 --save-dir outputs --no-show
```

## Sample Output: Hadamard Gate

For the included sample output, the Hadamard gate is applied to `|0>`.

The Hadamard operation creates:

```text
(|0> + |1>) / sqrt(2)
```

Therefore, the measurement probabilities are:

```text
P(|0>) = 0.5000  (50.0%)
P(|1>) = 0.5000  (50.0%)
```

The Bloch sphere visualization shows the final state pointing along the positive X axis, which is the expected state after applying `H` to `|0>`.

## Repository Submission Steps

1. Create a GitHub repository.
2. Push this project folder to that repository.
3. Confirm the source code, README/report, and `outputs/` images are visible on GitHub.
4. Share the GitHub repository link in the assignment submission channel on Discord.
