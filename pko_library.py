class PKOLibrary:
    @staticmethod
    def evaluate_all(claim_dict):
        v = []
        inputs = claim_dict.get("inputs", {})
        outputs = claim_dict.get("outputs", {})
        env = claim_dict.get("environment", {})

        e_in = inputs.get("energy_in_j", 0.0)
        e_out = outputs.get("energy_out_j", 0.0)
        v_in = inputs.get("voltage_v", 0.0)
        i_in = inputs.get("current_a", 0.0)
        p_out = outputs.get("power_out_w", 0.0)
        m_in = inputs.get("mass_in_kg", 0.0)
        m_out = outputs.get("mass_out_kg", 0.0)

        # 1. First Law (Energy Conservation)
        if e_out > e_in + 1e-2:
            v.append({"law": "TH-01", "message": "Energy output exceeds input."})
            
        # 2. Perpetual Motion (Energy from nothing)
        if e_in == 0 and e_out > 0:
            v.append({"law": "TH-05", "message": "Energy generated from nothing."})

        # 3. Electrical Power Limit (P <= V*I)
        p_in_elec = v_in * i_in
        if p_out > p_in_elec + 1e-2:
            v.append({"law": "EL-01", "message": "Power output exceeds V*I input."})

        # 4. Zero Voltage Power
        if p_in_elec == 0 and p_out > 0:
            v.append({"law": "EL-04", "message": "Electrical output without input."})

        # 5. Mass Conservation
        if m_out > m_in + 1e-2:
            v.append({"law": "ME-01", "message": "Mass creation detected."})

        # 6. Matter from Nothing
        if m_in == 0 and m_out > 0:
            v.append({"law": "ME-02", "message": "Mass output with zero input."})

        return v