"""
SEM Protocol - Benchmark do Axioma 07
Testa se o validate_plan() do memory_plugin.py funciona corretamente.
"""

import json
import os
import sys

# Aponta para a raiz do repositório onde está o memory_plugin.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from memory_plugin import SEMMemory

def run_benchmark():
    # Carrega os casos de teste
    test_file = os.path.join(os.path.dirname(__file__), 'ethical_test_cases.json')
    with open(test_file, 'r', encoding='utf-8') as f:
        test_cases = json.load(f)

    total = len(test_cases)
    passed = 0
    failed = 0

    sem = SEMMemory()

    print(f"\n{'='*60}")
    print(f"  SEM Benchmark - Axioma 07")
    print(f"  A correr {total} testes...")
    print(f"{'='*60}\n")

    for case in test_cases:
        is_valid, violations, action = sem.validate_plan(case['plan'])
        expected = case['expected_valid']

        if is_valid == expected:
            status = "✅ PASS"
            passed += 1
        else:
            status = "❌ FAIL"
            failed += 1

        print(f"{status} | {case['id']}")
        print(f"       {case['description']}")
        if violations:
            print(f"       Violações: {', '.join(violations)}")
        print()

    print(f"{'='*60}")
    print(f"  Resultado: {passed}/{total} testes passaram ({(passed/total)*100:.1f}%)")
    if failed == 0:
        print("  🏆 Axioma 07 validado sem falhas!")
    else:
        print(f"  ⚠️  {failed} teste(s) falharam.")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    run_benchmark()
