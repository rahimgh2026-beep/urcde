import json
from pko_library import PKOLibrary

def load_data(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def run():
    valid = load_data('datasets/valid_claims.json')
    invalid = load_data('datasets/invalid_claims.json')
    
    TP = TN = FP = FN = 0

    print("=" * 60)
    print("🔬 URCDE BENCHMARK LAB (Sprint 3.5)")
    print("=" * 60)

    # 1. بررسی پرونده‌های معتبر (باید PASS شوند)
    for case in valid:
        v = PKOLibrary.evaluate_all(case)
        if len(v) == 0:
            TN += 1
        else:
            FP += 1
            print(f"🔴 [FALSE POSITIVE] Valid claim rejected: {case['title']} -> {v[0]['message']}")

    # 2. بررسی پرونده‌های دروغین (باید REJECT شوند)
    for case in invalid:
        v = PKOLibrary.evaluate_all(case)
        if len(v) > 0:
            TP += 1
        else:
            FN += 1
            print(f"💥 [FALSE NEGATIVE] Invalid claim passed: {case['title']}")

    total = TP + TN + FP + FN
    accuracy = (TP + TN) / total * 100 if total > 0 else 0
    precision = (TP / (TP + FP) * 100) if (TP + FP) > 0 else 0
    recall = (TP / (TP + FN) * 100) if (TP + FN) > 0 else 0

    print("\n" + "=" * 60)
    print("📊 PERFORMANCE METRICS")
    print("=" * 60)
    print(f"Total Cases Tested : {total}")
    print(f"True Positives (TP): {TP} (Junk correctly blocked)")
    print(f"True Negatives (TN): {TN} (Good patents passed)")
    print(f"False Positives(FP): {FP} (Good patents wrongly blocked)")
    print(f"False Negatives(FN): {FN} (Junk slipped through!)")
    print("-" * 60)
    print(f"🎯 Accuracy  : {accuracy:.1f}%")
    print(f"🎯 Precision : {precision:.1f}%")
    print(f"🎯 Recall    : {recall:.1f}%")
    print("=" * 60)

if __name__ == "__main__":
    run()