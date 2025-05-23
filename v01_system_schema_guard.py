import os
import json
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMA_PATH = os.path.join(BASE_DIR, "system_schema.json")
MODULE_DIR = os.path.join(BASE_DIR, "modules")

def load_schema():
    with open(SCHEMA_PATH, "r") as f:
        return json.load(f)

def scan_module_files():
    return [f for f in os.listdir(MODULE_DIR) if f.endswith(".json")]

def fix_type(value, expected_type):
    if expected_type == "str":
        return str(value)
    elif expected_type == "float":
        try:
            return float(value)
        except:
            return 0.0
    elif expected_type == "int":
        try:
            return int(value)
        except:
            return 0
    elif expected_type == "bool":
        return bool(value)
    elif expected_type == "list":
        return value if isinstance(value, list) else []
    elif expected_type == "dict":
        return value if isinstance(value, dict) else {}
    else:
        return value

def repair_module(filepath, schema):
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
    except Exception as e:
        print(f"[ERROR] 無法讀取 {filepath}，自動刪除：{e}")
        os.remove(filepath)
        return

    repaired = False
    for key, expected_type in schema.items():
        if key not in data:
            data[key] = fix_type("", expected_type)
            repaired = True
        elif not isinstance(data[key], eval(expected_type)):
            data[key] = fix_type(data[key], expected_type)
            repaired = True

    if repaired:
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
        print(f"[REPAIRED] 修正完成：{filepath}")

def main():
    print(">>> v01_system_schema_guard.py 啟動")

    if not os.path.exists(SCHEMA_PATH):
        print(f"[ERROR] 找不到 schema 檔案：{SCHEMA_PATH}")
        return

    if not os.path.exists(MODULE_DIR):
        print(f"[ERROR] 找不到模組資料夾：{MODULE_DIR}")
        return

    schema = load_schema()
    module_files = scan_module_files()

    for fname in module_files:
        repair_module(os.path.join(MODULE_DIR, fname), schema)

    print(">>> v01 檢查與修復完畢")

if __name__ == "__main__":
    main()
