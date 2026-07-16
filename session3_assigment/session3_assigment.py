

from __future__ import annotations

from pathlib import Path
from typing import Callable

import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_histogram
from qiskit.result.counts import Counts
from qiskit_aer import AerSimulator

DEFAULT_SHOTS = 1024

try:
    OUTPUT_DIR = Path(__file__).resolve().parent / "qcl_output"
    OUTPUT_DIR.mkdir(exist_ok=True)
except OSError:
    OUTPUT_DIR = Path.cwd()


# ---------------------------------------------------------------------------
# 1. Circuit builders
# ---------------------------------------------------------------------------

def create_superposition(num_qubits: int = 1) -> QuantumCircuit:
   
    qc = QuantumCircuit(num_qubits, name="Superposition")
    for qubit in range(num_qubits):
        qc.h(qubit)
    return qc


def create_bell_state() -> QuantumCircuit:
  
    qc = QuantumCircuit(2, name="Bell State")
    qc.h(0)
    qc.cx(0, 1)
    return qc


def create_ghz_state(num_qubits: int = 3) -> QuantumCircuit:
    
    if num_qubits < 2:
        raise ValueError("GHZ state needs at least 2 qubits")
    qc = QuantumCircuit(num_qubits, name="GHZ State")
    qc.h(0)
    for qubit in range(1, num_qubits):
        qc.cx(0, qubit)
    return qc


# ---------------------------------------------------------------------------
# 2. Execution & display helpers
# ---------------------------------------------------------------------------

def run_circuit(circuit: QuantumCircuit, shots: int = DEFAULT_SHOTS) -> Counts:
  
    simulator = AerSimulator()
    measured = circuit.copy()
    measured.measure_all()
    transpiled = transpile(measured, simulator)
    result = simulator.run(transpiled, shots=shots).result()
    return result.get_counts()


def show_statevector(circuit: QuantumCircuit) -> Statevector:
   
    state = Statevector(circuit)
    print("\nStatevector (before measurement):")
    for label, amplitude in state.to_dict().items():
        probability = abs(amplitude) ** 2
        sign = "+" if amplitude.imag >= 0 else "-"
        print(
            f"  |{label}>   amplitude = {amplitude.real:+.4f} {sign} {abs(amplitude.imag):.4f}j"
            f"   probability = {probability * 100:5.1f}%"
        )
    return state


def show_histogram(counts: Counts, title: str = "Measurement Outcomes") -> None:
   
    print("\nMeasurement counts:")
    total = sum(counts.values())
    for outcome in sorted(counts):
        pct = 100 * counts[outcome] / total
        print(f"  |{outcome}>: {counts[outcome]:>5} shots ({pct:5.1f}%)")

    fig = plot_histogram(counts, title=title)

    try:
        filename = OUTPUT_DIR / f"{title.lower().replace(' ', '_')}_histogram.png"
        fig.savefig(filename, bbox_inches="tight")
        print(f"\nHistogram image saved to: {filename}")
    except OSError as exc:
        print(f"\n(could not save histogram image: {exc})")

    try:
        plt.show()
    except Exception:
        pass
    plt.close(fig)


# ---------------------------------------------------------------------------
# 3. Menu plumbing
# ---------------------------------------------------------------------------

MENU_TEXT = """
========== Quantum Circuit Library ==========

1. Superposition
2. Bell State
3. GHZ State
4. Exit
"""

EXPLANATIONS = {
    "Superposition": (
        "A single Hadamard gate splits the qubit evenly between |0> and |1>.\n"
        "With no entangling gate involved, each shot independently collapses\n"
        "to 0 or 1 with roughly 50% probability - the qubit only 'decides'\n"
        "its outcome at the moment of measurement."
    ),
    "Bell State": (
        "The Hadamard on qubit 0 followed by a CNOT to qubit 1 entangles the\n"
        "pair into (|00> + |11>) / sqrt(2). Because the qubits are correlated,\n"
        "only '00' and '11' should appear, each roughly half the time - you\n"
        "should never see '01' or '10'. Measuring one qubit instantly tells\n"
        "you the other's outcome, regardless of distance."
    ),
    "GHZ State": (
        "The same Hadamard + CNOT-chain pattern used for the Bell state is\n"
        "extended across all N qubits, entangling them into\n"
        "(|00...0> + |11...1>) / sqrt(2). Only the all-zeros and all-ones\n"
        "outcomes should appear, each roughly half the time - a direct\n"
        "generalization of 2-qubit entanglement to N qubits."
    ),
}


def run_demo(name: str, circuit: QuantumCircuit) -> None:
    
    print(f"\n{'-' * 60}")
    print(f"  {name}  ({circuit.num_qubits} qubit{'s' if circuit.num_qubits != 1 else ''})")
    print(f"{'-' * 60}")

    print("\nCircuit diagram:")
    print(circuit.draw(output="text"))

    show_statevector(circuit)

    counts = run_circuit(circuit)
    show_histogram(counts, title=name)

    print("\nExplanation:")
    print(EXPLANATIONS[name])


MENU_ACTIONS: dict[str, tuple[str, Callable[[], QuantumCircuit]]] = {
    "1": ("Superposition", create_superposition),
    "2": ("Bell State", create_bell_state),
    "3": ("GHZ State", create_ghz_state),
}


def main() -> None:
    print("Welcome to the Quantum Circuit Library!")
    while True:
        print(MENU_TEXT)
        choice = input("Select an option (1-4): ").strip()

        if choice == "4":
            print("\nExiting Quantum Circuit Library. Goodbye!")
            break

        action = MENU_ACTIONS.get(choice)
        if action is None:
            print("\nInvalid choice - please enter a number from 1 to 4.")
            continue

        name, factory = action
        run_demo(name, factory())
        input("\nPress Enter to return to the menu...")


if __name__ == "__main__":
    main()