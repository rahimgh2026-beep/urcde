import json
from pydantic import BaseModel, Field

# ==========================================
# ۱. قرارداد داده (JSON Schema - Data Contract)
# ==========================================
class Inputs(BaseModel):
    energy_in_j: float = Field(default=0.0, description="Input energy in Joules")
    mass_in_kg: float = Field(default=0.0, description="Input mass in kg")
    voltage_v: float = Field(default=0.0, description="Input voltage")
    current_a: float = Field(default=0.0, description="Input current in Amperes")

class Outputs(BaseModel):
    energy_out_j: float = Field(default=0.0, description="Output energy (or work) in Joules")
    mass_out_kg: float = Field(default=0.0, description="Output mass in kg")
    power_out_w: float = Field(default=0.0, description="Output power in Watts")

class Environment(BaseModel):
    temperature_hot_k: float = Field(default=298.15, description="Hot reservoir temp in Kelvin")
    temperature_cold_k: float = Field(default=298.15, description="Cold reservoir temp in Kelvin")

class Claim(BaseModel):
    claim_id: str
    title: str
    domain: str
    inputs: Inputs
    outputs: Outputs
    environment: Environment

# ==========================================
# ۲. موتور دیکتاتور فیزیک (Constraint Engine & PKO Library)
# ==========================================
class ConstraintEngine:
    def evaluate(self, claim: Claim) -> dict:
        violations = []
        
        # اجرای ۵ قانون طلایی
        checks = [
            self._check_conservation_of_energy(claim),
            self._check_carnot_limit(claim),
            self._check_mass_conservation(claim),
            self._check_ohms_law_power(claim),
            self._check_absolute_zero(claim)
        ]
        
        for check in checks:
            if check["status"] == "VIOLATED":
                violations.append(check)
                
        return {
            "claim_id": claim.claim_id,
            "title": claim.title,
            "overall_status": "REJECTED_PHYSICS_VIOLATION" if violations else "PASS",
            "violations": violations
        }

    def _check_conservation_of_energy(self, claim: Claim):
        if claim.outputs.energy_out_j > claim.inputs.energy_in_j:
            return {
                "law": "CONSERVATION_OF_ENERGY",
                "status": "VIOLATED",
                "severity": "CRITICAL",
                "message": f"Energy out ({claim.outputs.energy_out_j}J) exceeds energy in ({claim.inputs.energy_in_j}J)."
            }
        return {"law": "CONSERVATION_OF_ENERGY", "status": "PASS"}

    def _check_carnot_limit(self, claim: Claim):
        th = claim.environment.temperature_hot_k
        tc = claim.environment.temperature_cold_k
        
        if claim.inputs.energy_in_j > 0 and th > tc:
            carnot_eff = 1.0 - (tc / th)
            claimed_eff = claim.outputs.energy_out_j / claim.inputs.energy_in_j
            if claimed_eff > carnot_eff:
                return {
                    "law": "SECOND_LAW_CARNOT_LIMIT",
                    "status": "VIOLATED",
                    "severity": "CRITICAL",
                    "message": f"Claimed efficiency ({claimed_eff:.2%}) exceeds Carnot limit ({carnot_eff:.2%})."
                }
        return {"law": "SECOND_LAW_CARNOT_LIMIT", "status": "PASS"}

    def _check_mass_conservation(self, claim: Claim):
        if claim.outputs.mass_out_kg > claim.inputs.mass_in_kg:
            return {
                "law": "MASS_CONSERVATION",
                "status": "VIOLATED",
                "severity": "CRITICAL",
                "message": "Output mass exceeds input mass (Matter creation detected)."
            }
        return {"law": "MASS_CONSERVATION", "status": "PASS"}

    def _check_ohms_law_power(self, claim: Claim):
        expected_power = claim.inputs.voltage_v * claim.inputs.current_a
        if expected_power > 0 and claim.outputs.power_out_w > expected_power:
            return {
                "law": "OHMS_LAW_POWER_LIMIT",
                "status": "VIOLATED",
                "severity": "CRITICAL",
                "message": f"Output power ({claim.outputs.power_out_w}W) exceeds electrical input ({expected_power}W)."
            }
        return {"law": "OHMS_LAW_POWER_LIMIT", "status": "PASS"}

    def _check_absolute_zero(self, claim: Claim):
        if claim.environment.temperature_hot_k < 0 or claim.environment.temperature_cold_k < 0:
            return {
                "law": "ABSOLUTE_ZERO_LIMIT",
                "status": "VIOLATED",
                "severity": "CRITICAL",
                "message": "System claims to operate below 0 Kelvin."
            }
        return {"law": "ABSOLUTE_ZERO_LIMIT", "status": "PASS"}

# ==========================================
# ۳. مجموعه تست‌های واقعی (10 Test Cases)
# ==========================================
def run_test_suite():
    engine = ConstraintEngine()
    
    test_cases = [
        {"claim_id": "C-01", "title": "Infinite Generator", "domain": "thermodynamics", "inputs": {"energy_in_j": 100}, "outputs": {"energy_out_j": 200}, "environment": {}},
        {"claim_id": "C-02", "title": "Standard Diesel Engine", "domain": "thermodynamics", "inputs": {"energy_in_j": 1000}, "outputs": {"energy_out_j": 350}, "environment": {"temperature_hot_k": 800, "temperature_cold_k": 300}},
        {"claim_id": "C-03", "title": "Super Efficient Stirling Engine", "domain": "thermodynamics", "inputs": {"energy_in_j": 100}, "outputs": {"energy_out_j": 40}, "environment": {"temperature_hot_k": 400, "temperature_cold_k": 300}},
        {"claim_id": "C-04", "title": "Quantum Matter Replicator", "domain": "mechanics", "inputs": {"mass_in_kg": 5}, "outputs": {"mass_out_kg": 6}, "environment": {}},
        {"claim_id": "C-05", "title": "Zero-Point Amplifier", "domain": "electronics", "inputs": {"voltage_v": 10, "current_a": 2}, "outputs": {"power_out_w": 50}, "environment": {}},
        {"claim_id": "C-06", "title": "LED Driver Circuit", "domain": "electronics", "inputs": {"voltage_v": 5, "current_a": 1}, "outputs": {"power_out_w": 4.5}, "environment": {}},
        {"claim_id": "C-07", "title": "Sub-Void Cryocooler", "domain": "thermodynamics", "inputs": {"energy_in_j": 500}, "outputs": {"energy_out_j": 100}, "environment": {"temperature_hot_k": 300, "temperature_cold_k": -5}},
        {"claim_id": "C-08", "title": "Membrane Water Purifier", "domain": "fluid_dynamics", "inputs": {"mass_in_kg": 10}, "outputs": {"mass_out_kg": 9.5}, "environment": {}},
        {"claim_id": "C-09", "title": "Vacuum Energy Harvester", "domain": "quantum", "inputs": {"energy_in_j": 0}, "outputs": {"energy_out_j": 50}, "environment": {}},
        {"claim_id": "C-10", "title": "Steam Power Plant", "domain": "thermodynamics", "inputs": {"energy_in_j": 1000}, "outputs": {"energy_out_j": 450}, "environment": {"temperature_hot_k": 700, "temperature_cold_k": 300}}
    ]

    print("🚀 URCDE Sprint-1: Executing Risk Reports...\n" + "-"*50)
    for data in test_cases:
        claim_obj = Claim(**data)
        report = engine.evaluate(claim_obj)
        
        status_icon = "✅" if report["overall_status"] == "PASS" else "❌"
        print(f"{status_icon} Case: {report['title']} ({report['claim_id']}) -> {report['overall_status']}")
        if report["violations"]:
            for v in report["violations"]:
                print(f"    ⚠️  {v['law']}: {v['message']}")

if __name__ == "__main__":
    run_test_suite()