from qiskit import QuantumCircuit
from qiskit.visualization import plot_bloch_multivector
from qiskit.quantum_info import Statevector
import matplotlib.pyplot as plt

GATES = {
    "1": "X Gate",
    "2": "Y Gate",
    "3": "Z Gate",
    "4": "H (Hadamard) Gate",
    "5": "RY Gate",
}


def choose_gate():
    print("\nChoose a quantum gate:")
    for key, name in GATES.items():
        print(f"  {key}. {name}")

    while True:
        choice = input("Enter choice (1-5): ").strip()
        if choice in GATES:
            return choice
        print("  Invalid choice, try again.")


def build_circuit(choice):
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
        while True:
            try:
                theta = float(input("Enter rotation angle θ (radians): "))
                break
            except ValueError:
                print("  Please enter a number.")
        qc.ry(theta, 0)

    return qc


def get_probabilities(qc):
    sv = Statevector.from_instruction(qc)
    probs = sv.probabilities()
    return probs[0], probs[1]


def main():
    print("=" * 40)
    print("  Single-Qubit Gate Explorer")
    print("=" * 40)

    choice = choose_gate()
    gate_name = GATES[choice]
    qc = build_circuit(choice)

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
    fig.suptitle(f"Bloch Sphere — {gate_name}", fontsize=13)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    while True:
        main()
        again = input("\nTry another gate? (y/n): ").strip().lower()
        if again != "y":
            print("Bye!")
            break
