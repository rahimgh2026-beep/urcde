import os
from pko_library import PKOLibrary

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clear_screen()
    print("=" * 60)
    print("🚀 URCDE - IP INTELLIGENCE ENGINE (OFFLINE TERMINAL)")
    print("=" * 60)
    print("Welcome, Commander. Enter patent claim data to evaluate.")
    print("Type 'exit' in the title to close the system.")

    while True:
        print("\n" + "-" * 60)
        title = input("📝 Claim Title: ")
        if title.lower() == 'exit':
            print("System shutting down. Goodbye.")
            break

        print("\n--- Enter Values (Press ENTER to leave as 0) ---")
        try:
            e_in  = float(input("📥 Energy Input (Joules)  : ") or 0)
            e_out = float(input("📤 Energy Output (Joules) : ") or 0)
            v_in  = float(input("⚡ Voltage Input (Volts)  : ") or 0)
            i_in  = float(input("🔌 Current Input (Amps)   : ") or 0)
            p_out = float(input("💡 Power Output (Watts)   : ") or 0)
            m_in  = float(input("🧱 Mass Input (kg)        : ") or 0)
            m_out = float(input("📦 Mass Output (kg)       : ") or 0)
        except ValueError:
            print("⚠️ ERROR: Please enter only numbers. Let's try again.")
            continue

        claim_data = {
            "inputs": {"energy_in_j": e_in, "voltage_v": v_in, "current_a": i_in, "mass_in_kg": m_in},
            "outputs": {"energy_out_j": e_out, "power_out_w": p_out, "mass_out_kg": m_out},
            "environment": {}
        }

        print("\n⚖️ EVALUATING THROUGH PKO-15 ENGINE...")
        violations = PKOLibrary.evaluate_all(claim_data)

        if len(violations) == 0:
            print("🟢 VERDICT: PASS (Scientifically Plausible)")
        else:
            print("🔴 VERDICT: REJECTED (Physics Violation Detected)")
            for v in violations:
                print(f"   ⚠️  [{v['law']}] -> {v['message']}")

if __name__ == "__main__":
    main()