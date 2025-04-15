# 🦆 DuckDB Ingestion Profiling & Benchmark

This project provides a reproducible pipeline to benchmark and analyze the ingestion performance of [DuckDB](https://duckdb.org/) using various CSV datasets. It includes ingestion automation, JSON-based profiling extraction, and visual operator-level execution time breakdowns.

---

## 📦 Features

- ✅ Automated ingestion benchmark with `benchmark.py`
- ✅ JSON-based profiling via DuckDB's built-in profiler
- ✅ Visualization of operator-level execution time (`READ_CSV_AUTO`, `CREATE TABLE`, etc.)
- ✅ Modular and extensible: easy to plug in larger datasets or new profiling metrics

---

## 🛠️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/duckdb-ingestion.git
cd duckdb-ingestion