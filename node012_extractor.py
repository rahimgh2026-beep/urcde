import os
import json
from google import genai
from dotenv import load_dotenv

# بارگذاری امن کلید API
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ Error: GEMINI_API_KEY not found in .env file.")
    exit()

# اتصال با کتابخانه مدرن و جدید گوگل
client = genai.Client(api_key=api_key)

class Node012Extractor:
    def extract_from_text(self, raw_claim_text: str) -> dict:
        prompt = f"""
        You are Node-012, a highly precise physics data extractor.
        Read the following raw patent claim.
        Extract the physical variables and return ONLY a valid JSON object.
        Do not include markdown tags like ```json. Just the raw JSON string.

        The JSON must strictly follow this structure:
        {{
            "claim_id": "AUTO-GEN-001",
            "title": "<extract a short title>",
            "domain": "thermodynamics",
            "inputs": {{
                "energy_in_j": <float, default 0.0>,
                "mass_in_kg": <float, default 0.0>,
                "voltage_v": <float, default 0.0>,
                "current_a": <float, default 0.0>
            }},
            "outputs": {{
                "energy_out_j": <float, default 0.0>,
                "mass_out_kg": <float, default 0.0>,
                "power_out_w": <float, default 0.0>
            }},
            "environment": {{
                "temperature_hot_k": <float, default 298.15>,
                "temperature_cold_k": <float, default 298.15>
            }}
        }}

        Raw Patent Claim:
        "{raw_claim_text}"
        """

        try:
            # ارسال درخواست به جدیدترین مدل گوگل
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )
            
            # پاک‌سازی خروجی برای اطمینان از فرمت صحیح JSON
            clean_json_str = response.text.replace("```json", "").replace("```", "").strip()
            extracted_data = json.loads(clean_json_str)
            return extracted_data
            
        except Exception as e:
            print(f"❌ Extraction failed: {e}")
            return None

# ==========================================
# 🧪 تست زنده استخراج‌گر
# ==========================================
if __name__ == "__main__":
    extractor = Node012Extractor()
    
    test_inventor_text = """
    I have invented a revolutionary perpetual motion heat amplifier. 
    It takes in exactly 100 Joules of heat energy from a warm room. 
    Using my secret magnetic flux technology, it outputs an incredible 250 Joules of mechanical work!
    """
    
    print("\n📡 Sending raw text to Gemini 2.0 Flash...\n")
    print(f"RAW TEXT: {test_inventor_text}")
    print("-" * 50)
    
    structured_data = extractor.extract_from_text(test_inventor_text)
    
    if structured_data:
        print("\n✅ AI Extracted Structured Data:")
        print(json.dumps(structured_data, indent=4))
    else:
        print("\n❌ Failed to extract data.")