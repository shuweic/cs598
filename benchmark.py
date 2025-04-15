import subprocess
import os
import time
import json
import uuid

# DuckDB CLI 可执行文件（若在 PATH 中，保持为 duckdb 即可）
DUCKDB_CLI = "duckdb"

# 每次使用不同的临时数据库文件，避免文件锁冲突
DB_FILE = f"temp_{uuid.uuid4().hex}.duckdb"

# 文件夹路径
DATA_DIR = "./data"
OUTPUT_DIR = "./profile_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Benchmark 文件列表（请确保这些 CSV 文件已存在于 data/ 文件夹）
csv_files = [
    "10MB.csv",
    "100MB.csv",
]

for csv in csv_files:
    print(f"\n🚀 Running benchmark for {csv}...")

    profile_file = f"profile_{csv}.json"
    profile_path = os.path.join(OUTPUT_DIR, profile_file)

    # 构造 SQL 脚本
    sql = f"""
    SET enable_profiling = JSON;
    SET profiling_output = '{profile_path}';

    DROP TABLE IF EXISTS t;
    CREATE TABLE t AS SELECT * FROM read_csv_auto('{DATA_DIR}/{csv}');
    """

    # 写入 SQL 文件
    sql_file = f"temp_sql_{uuid.uuid4().hex}.sql"
    with open(sql_file, "w") as f:
        f.write(sql)

    # 运行 CLI 命令
    start = time.time()
    result = subprocess.run([DUCKDB_CLI, DB_FILE, "-init", sql_file], capture_output=True, text=True)
    duration = time.time() - start

    print(f"⏱️  Ingestion time: {duration:.2f} seconds")

    # 输出 CLI 错误（如果有）
    if result.stderr:
        print(f"⚠️  CLI stderr:\n{result.stderr.strip()}")

    # 解析 profiling 输出
    if os.path.exists(profile_path):
        try:
            with open(profile_path) as f:
                profile_data = json.load(f)
                exec_time = profile_data.get("result", {}).get("timing", {}).get("execution_time", "N/A")
                print(f"📊 Profiling execution_time: {exec_time}")
        except json.JSONDecodeError:
            print("❌ Profiling output is not valid JSON. Please check DuckDB stderr above.")
    else:
        print("❌ Profiling JSON file was not generated.")

    # 清理 SQL 文件（如需保留可注释掉）
    os.remove(sql_file)

# 如果你愿意，也可以最后删除临时数据库文件
# os.remove(DB_FILE)