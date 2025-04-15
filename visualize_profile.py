import json
import os
import matplotlib.pyplot as plt

PROFILE_DIR = "profile_output"

def load_profile(file_path):
    with open(file_path) as f:
        data = json.load(f)
    return data

def extract_operator_times_recursive(node, result):
    """递归提取所有 operator_name 和 operator_timing"""
    name = node.get("operator_name", "Unknown").strip()
    timing = node.get("operator_timing", 0.0)
    result.append((name, timing))
    for child in node.get("children", []):
        extract_operator_times_recursive(child, result)

def extract_all_operator_timings(profile_data):
    result = []
    for child in profile_data.get("children", []):
        extract_operator_times_recursive(child, result)
    return result

def plot_operator_times(timings, title):
    operators = [op for op, _ in timings]
    times = [t for _, t in timings]

    plt.figure(figsize=(10, 6))
    plt.barh(operators, times)
    plt.xlabel("Execution Time (s)")
    plt.title(f"DuckDB Ingestion Operator Time - {title}")
    plt.tight_layout()
    plt.show()

def main():
    files = [f for f in os.listdir(PROFILE_DIR) if f.endswith(".json")]
    if not files:
        print("⚠️ No profile JSON files found in 'profile_output/'")
        return

    for f in files:
        print(f"📊 Processing: {f}")
        path = os.path.join(PROFILE_DIR, f)
        data = load_profile(path)
        timings = extract_all_operator_timings(data)
        if timings:
            plot_operator_times(timings, f.replace("profile_", "").replace(".json", ""))
        else:
            print(f"❌ No operator timings found in {f}")

if __name__ == "__main__":
    main()