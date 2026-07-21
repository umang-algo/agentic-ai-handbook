"""
The Practitioner's Coding Handbook of Agentic AI — Master Interactive CLI Launcher
===================================================================================
Master interactive CLI tool for Students, Researchers, and AI Engineers.

Usage:
    python main.py list             # List all 21 chapters & code modules
    python main.py run <ch_name>    # Run interactive lab for a chapter (e.g. ch01, ch03, ch19)
    python main.py bench <ch_name>  # Run empirical benchmark experiment
    python main.py test             # Run automated verification across all 21 chapters

From: The Practitioner's Handbook of Agentic AI
"""

import sys
import os
import argparse
import subprocess
import py_compile
from typing import List, Dict, Any

# Add coding-handbook to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from common.logger import AgentLogger, Colors


CHAPTER_MAP = {
    "ch01": "ch01_llm_anatomy",
    "ch02": "ch02_reasoning",
    "ch03": "ch03_react",
    "ch04": "ch04_tool_calling",
    "ch05": "ch05_embeddings",
    "ch06": "ch06_vector_db",
    "ch07": "ch07_context_assembly",
    "ch08": "ch08_code_interpreter",
    "ch09": "ch09_mcp",
    "ch10": "ch10_multi_agent",
    "ch11": "ch11_ai_ides",
    "ch12": "ch12_agentic_sdks",
    "ch13": "ch13_enterprise_architectures",
    "ch14": "ch14_evaluation",
    "ch15": "ch15_observability",
    "ch16": "ch16_economics",
    "ch17": "ch17_fine_tuning",
    "ch18": "ch18_github_agent",
    "ch19": "ch19_production_industries",
    "ch20": "ch20_ai_harness_tools",
    "ch21": "ch21_evaluating_ai",
}


def resolve_chapter_folder(target: str) -> str:
    target_lower = target.lower().strip()
    if target_lower in CHAPTER_MAP:
        return CHAPTER_MAP[target_lower]
    for key, val in CHAPTER_MAP.items():
        if val == target_lower or target_lower in val:
            return val
    return target_lower


def cmd_list():
    AgentLogger.title("Practitioner's Handbook of Agentic AI — Chapter Index")
    base_dir = os.path.dirname(os.path.abspath(__file__))

    for key in sorted(CHAPTER_MAP.keys(), key=lambda x: int(x.replace("ch", ""))):
        folder_name = CHAPTER_MAP[key]
        full_path = os.path.join(base_dir, folder_name)
        if os.path.exists(full_path):
            py_files = [f for f in sorted(os.listdir(full_path)) if f.endswith(".py")]
            print(f"{Colors.BOLD}{key.upper()}{Colors.ENDC} ({Colors.OKCYAN}{folder_name}{Colors.ENDC}):")
            for py in py_files:
                print(f"  └─ {Colors.OKGREEN}{py}{Colors.ENDC}")
            print()


def cmd_run(target: str):
    folder_name = resolve_chapter_folder(target)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, folder_name)

    if not os.path.exists(full_path):
        AgentLogger.error(f"Chapter folder '{target}' not found.")
        sys.exit(1)

    AgentLogger.title(f"Running Chapter Lab: {folder_name}")
    py_files = [f for f in sorted(os.listdir(full_path)) if f.endswith(".py")]

    if not py_files:
        AgentLogger.warning("No Python scripts found in this chapter.")
        return

    for py in py_files:
        script_path = os.path.join(full_path, py)
        AgentLogger.section(f"Executing: {py}")
        res = subprocess.run([sys.executable, script_path])
        if res.returncode == 0:
            AgentLogger.success(f"Finished executing {py}")
        else:
            AgentLogger.error(f"Execution failed for {py}")


def cmd_bench(target: str):
    folder_name = resolve_chapter_folder(target)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, folder_name)

    if not os.path.exists(full_path):
        AgentLogger.error(f"Chapter folder '{target}' not found.")
        sys.exit(1)

    AgentLogger.title(f"Running Empirical Benchmark: {folder_name}")
    py_files = [f for f in sorted(os.listdir(full_path)) if f.endswith(".py")]

    for py in py_files:
        script_path = os.path.join(full_path, py)
        AgentLogger.section(f"Benchmark Test: {py}")
        subprocess.run([sys.executable, script_path])


def cmd_test():
    AgentLogger.title("Automated Test Runner Across All 21 Chapters")
    base_dir = os.path.dirname(os.path.abspath(__file__))

    total_files = 0
    passed = 0
    failed = 0

    for key, folder_name in CHAPTER_MAP.items():
        full_path = os.path.join(base_dir, folder_name)
        if not os.path.exists(full_path):
            continue

        py_files = [f for f in sorted(os.listdir(full_path)) if f.endswith(".py")]
        for py in py_files:
            total_files += 1
            script_path = os.path.join(full_path, py)
            try:
                py_compile.compile(script_path, doraise=True)
                res = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
                if res.returncode == 0:
                    AgentLogger.success(f"[{folder_name}] {py}")
                    passed += 1
                else:
                    AgentLogger.error(f"[{folder_name}] {py} EXEC ERROR:\n{res.stderr}")
                    failed += 1
            except Exception as e:
                AgentLogger.error(f"[{folder_name}] {py} COMPILE ERROR: {e}")
                failed += 1

    AgentLogger.section("Test Execution Summary")
    print(f"Total Modules Tested: {total_files}")
    print(f"Passed: {Colors.OKGREEN}{passed}{Colors.ENDC}")
    print(f"Failed: {Colors.FAIL}{failed}{Colors.ENDC}")

    if failed == 0:
        AgentLogger.success("All 21 chapter modules passed verification!")
    else:
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Practitioner's Coding Handbook Master CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    subparsers.add_parser("list", help="List all chapters and code modules")
    
    run_parser = subparsers.add_parser("run", help="Run interactive lab for a chapter")
    run_parser.add_argument("chapter", type=str, help="Chapter identifier (e.g. ch01, ch03, ch19)")

    bench_parser = subparsers.add_parser("bench", help="Run empirical benchmark experiment")
    bench_parser.add_argument("chapter", type=str, help="Chapter identifier (e.g. ch01, ch06, ch21)")

    subparsers.add_parser("test", help="Run automated test suite across all 21 chapters")

    args = parser.parse_args()

    if args.command == "list":
        cmd_list()
    elif args.command == "run":
        cmd_run(args.chapter)
    elif args.command == "bench":
        cmd_bench(args.chapter)
    elif args.command == "test":
        cmd_test()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
