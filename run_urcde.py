import json
# وارد کردن موتور فیزیک و قرارداد داده از اسپرینت ۱
from urcde_core import Claim, ConstraintEngine

class MockNode012:
    """
    شبیه‌ساز هوش مصنوعی:
    در نسخه تجاری، این کلاس به سرورهای OpenAI متصل می‌شود.
    در حال حاضر، ما وظیفه هوش مصنوعی را برای سیستم شبیه‌سازی می‌کنیم 
    تا خط لوله (Pipeline) پروژه متوقف نشود.
    """
    def extract_from_text(self, raw_text: str) -> dict:
        print("🤖 [Node-012 AI] Processing raw text...")
        
        # فرض می‌کنیم هوش مصنوعی متن را خوانده و این JSON را تولید کرده است:
        extracted_json = {
            "claim_id": "AUTO-GEN-001",
            "title": "Perpetual Motion Heat Amplifier",
            "domain": "thermodynamics",
            "inputs": {
                "energy_in_j": 100.0, 
                "mass_in_kg": 0.0, 
                "voltage_v": 0.0, 
                "current_a": 0.0
            },
            "outputs": {
                "energy_out_j": 250.0, # ادعای تولید ۲۵۰ ژول از ۱۰۰ ژول!
                "mass_out_kg": 0.0, 
                "power_out_w": 0.0
            },
            "environment": {
                "temperature_hot_k": 298.15, 
                "temperature_cold_k": 298.15
            }
        }
        return extracted_json

# ==========================================
# ⚙️ اجرای موتور اصلی URCDE
# ==========================================
if __name__ == "__main__":
    print("=" * 60)
    print("🚀 URCDE PIPELINE INITIALIZED (SPRINT 1 + SPRINT 2)")
    print("=" * 60)

    # 1. متن خام از طرف مخترع
    inventor_text = """
    I have invented a revolutionary perpetual motion heat amplifier. 
    It takes in exactly 100 Joules of heat energy from a warm room. 
    Using my secret magnetic flux technology, it outputs an incredible 250 Joules of mechanical work!
    """
    print(f"\n📩 INCOMING CLAIM:\n{inventor_text.strip()}")
    print("-" * 60)

    # 2. استخراج داده‌ها توسط Node 012
    extractor = MockNode012()
    structured_data = extractor.extract_from_text(inventor_text)
    print("\n✅ AI EXTRACED DATA (Claim Schema):")
    print(json.dumps(structured_data, indent=2))
    print("-" * 60)

    # 3. ارسال به موتور دیکتاتور فیزیک (اسپرینت ۱)
    print("\n⚖️ SENDING TO PHYSICS CONSTRAINT ENGINE (Node-013)...")
    engine = ConstraintEngine()
    
    # تبدیل دیکشنری به شیء استاندارد سیستم
    claim_obj = Claim(**structured_data)
    
    # صدور حکم
    report = engine.evaluate(claim_obj)

    # 4. چاپ گزارش نهایی
    status_icon = "🟢" if report["overall_status"] == "PASS" else "🔴"
    print(f"\n{status_icon} FINAL VERDICT: {report['overall_status']}")
    
    if report["violations"]:
        for v in report["violations"]:
            print(f"   ⚠️  [{v['law']}] -> {v['message']}")
    
    print("\n" + "=" * 60)