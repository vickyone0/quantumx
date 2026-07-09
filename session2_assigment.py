import argparse
from pathlib import Path

import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector

GATES = {
    "1": "X Gate",
    "2": "Y Gate",
    "3": "Z Gate",
    "4": "H (Hadamard) Gate",
    "5": "RY Gate",
}


def normalize_gate_choice(gate):
    aliases = {
        "x": "1",
        "y": "2",
        "z": "3",
        "h": "4",
        "hadamard": "4",
        "ry": "5",
    }

    normalized = str(gate).strip().lower()
    if normalized in GATES:
        return normalized
    if normalized in aliases:
        return aliases[normalized]
    raise ValueError("Gate must be one of: x, y, z, h, ry, or 1-5.")


def choose_gate():
    print("\nChoose a quantum gate:")
    for key, name in GATES.items():
        print(f"  {key}. {name}")

    while True:
        choice = input("Enter choice (1-5): ").strip()
        if choice in GATES:
            return choice
        print("  Invalid choice, try again.")


def choose_theta():
    while True:
        try:
            return float(input("Enter rotation angle theta (radians): "))
        except ValueError:
            print("  Please enter a number.")


def build_circuit(choice, theta=None):
    qc = QuantumCircuit(1)

    if choice == "1":
        qc.x(0)
    elif choice == "2":
        qc.y(0)
    elif choice == "3":
        qc.z(0)
    elif choice == "4":
        qc.h(0)
    elif choice == "5":
        if theta is None:
            theta = choose_theta()
        qc.ry(theta, 0)

    return qc


def get_probabilities(qc):
    sv = Statevector.from_instruction(qc)
    probs = sv.probabilities()
    return probs[0], probs[1]


def save_outputs(qc, gate_name, save_dir):
    save_path = Path(save_dir)
    save_path.mkdir(parents=True, exist_ok=True)

    circuit_fig = qc.draw(output="mpl")
    circuit_fig.savefig(save_path / "quantum_circuit.png", bbox_inches="tight", dpi=180)
    plt.close(circuit_fig)

    sv = Statevector.from_instruction(qc)
    bloch_fig = plot_bloch_multivector(sv)
    bloch_fig.suptitle(f"Bloch Sphere - {gate_name}", fontsize=13)
    bloch_fig.savefig(save_path / "bloch_sphere.png", bbox_inches="tight", dpi=180)
    plt.close(bloch_fig)

    p0, p1 = get_probabilities(qc)
    prob_fig, ax = plt.subplots(figsize=(5.5, 3.5))
    bars = ax.bar(["|0>", "|1>"], [p0, p1], color=["#2f6f73", "#d96c4a"])
    ax.set_ylim(0, 1)
    ax.set_ylabel("Probability")
    ax.set_title(f"Measurement Probabilities - {gate_name}")
    ax.grid(axis="y", alpha=0.25)
    for bar, value in zip(bars, [p0, p1]):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.03,
            f"{value:.4f}",
            ha="center",
            va="bottom",
        )
    prob_fig.savefig(save_path / "measurement_probabilities.png", bbox_inches="tight", dpi=180)
    plt.close(prob_fig)

    with (save_path / "console_output.txt").open("w", encoding="utf-8") as handle:
        handle.write(f"Circuit after applying {gate_name}:\n")
        handle.write(str(qc.draw(output="text")))
        handle.write("\n\nMeasurement probabilities:\n")
        handle.write(f"  P(|0>) = {p0:.4f}  ({p0 * 100:.1f}%)\n")
        handle.write(f"  P(|1>) = {p1:.4f}  ({p1 * 100:.1f}%)\n")


def run_once(choice=None, theta=None, save_dir=None, show=True):
    print("=" * 40)
    print("  Single-Qubit Gate Explorer")
    print("=" * 40)

    if choice is None:
        choice = choose_gate()
    else:
        choice = normalize_gate_choice(choice)
    gate_name = GATES[choice]
    qc = build_circuit(choice, theta)

    # --- Circuit diagram ---
    print(f"\nCircuit after applying {gate_name}:")
    print(qc.draw(output="text"))

    # --- Probabilities ---
    p0, p1 = get_probabilities(qc)
    print(f"\nMeasurement probabilities:")
    print(f"  P(|0⟩) = {p0:.4f}  ({p0*100:.1f}%)")
    print(f"  P(|1⟩) = {p1:.4f}  ({p1*100:.1f}%)")

    # --- Bloch sphere ---
    sv = Statevector.from_instruction(qc)
    fig = plot_bloch_multivector(sv)
    fig.suptitle(f"Bloch Sphere - {gate_name}", fontsize=13)
    plt.tight_layout()
    if save_dir:
        save_outputs(qc, gate_name, save_dir)
        print(f"\nSaved output files in: {Path(save_dir).resolve()}")
    if show:
        plt.show()
    else:
        plt.close(fig)


def parse_args():
    parser = argparse.ArgumentParser(description="Explore one-qubit quantum gates.")
    parser.add_argument("--gate", help="Gate to apply: x, y, z, h, ry, or 1-5.")
    parser.add_argument("--theta", type=float, help="Rotation angle in radians for the RY gate.")
    parser.add_argument("--save-dir", help="Directory for generated circuit, Bloch sphere, and probability images.")
    parser.add_argument("--no-show", action="store_true", help="Do not open Matplotlib windows.")
    return parser.parse_args()


def main():
    args = parse_args()

    if args.gate:
        run_once(args.gate, theta=args.theta, save_dir=args.save_dir, show=not args.no_show)
        return

    while True:
        run_once(save_dir=args.save_dir, show=not args.no_show)
        again = input("\nTry another gate? (y/n): ").strip().lower()
        if again != "y":
            print("Bye!")
            break


if __name__ == "__main__":
    main()
