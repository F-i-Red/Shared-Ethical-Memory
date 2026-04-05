import json
import sys
import os

# Adiciona a pasta raiz ao path para conseguires importar os teus módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ==========================================================
// TODO: AQUI TENS DE IMPORTAR O TEU MÓDULO
// Exemplo: from src.ethical_filter import EthicalArbiter
// Substitui a linha abaixo pelo teu import correto
import seu_modulo_de_memoria 
# ==========================================================

def run_ethical_benchmark():
    # Caminho para o ficheiro de testes que criámos
    test_file_path = os.path.join(os.path.dirname(__file__), 'ethical_test_cases.json')
    
    with open(test_file_path, 'r', encoding='utf-8') as f:
        test_cases = json.load(f)

    total_tests = len(test_cases)
    passed_tests = 0
    failed_tests = 0
    details = []

    print(f"Iniciando Benchmark Ético com {total_tests} casos...\n")

    for case in test_cases:
        case_id = case['id']
        input_text = case['input_text']
        expected = case['expected_decision']

        # ==========================================================
        // TODO: AQUI TENS DE CHAMAR A TUA FUNÇÃO
        // Tu tens uma função que recebe um texto e devolve "ALLOW" ou "BLOCK"?
        // Substitui esta linha pela chamada real à tua função.
        // Exemplo: result = ethical_arbiter.evaluate(input_text)
        
        # Simulação provisória (APAGAR DEPOIS)
        result = "ALLOW" 
        # ==========================================================

        # Avaliação
        if result.strip().upper() == expected:
            status = "✅ PASS"
            passed_tests += 1
        else:
            status = "❌ FAIL"
            failed_tests += 1

        details.append(f"{status} | ID: {case_id} | Esperado: {expected} | Obtido: {result}\n  Texto: {input_text[:60]}...")

    # Resultado Final
    print("-" * 50)
    for detail in details:
        print(detail)
    print("-" * 50)
    print(f"\nResultado Final: {passed_tests}/{total_tests} testes passaram ({(passed_tests/total_tests)*100:.1f}%)")
    
    if failed_tests > 0:
        print(f"⚠️  {failed_tests} testes falharam. O teu filtro ético precisa de ajustes.")

if __name__ == "__main__":
    run_ethical_benchmark()
