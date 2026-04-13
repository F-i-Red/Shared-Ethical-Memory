from structured_ethical_memory import StructuredEthicalMemory

structured = StructuredEthicalMemory()

exemplos = [
    {"principle": "Minimizar dano humano", "context": "Utilizador pediu instruções para algo perigoso", "decision": "Recusado", "justification": "Prioridade à segurança e não causar dano", "confidence": 0.92},
    {"principle": "Respeitar autonomia", "context": "Utilizador pediu para mentir em nome dele", "decision": "Recusado parcialmente", "justification": "Mentira pode violar confiança a longo prazo", "confidence": 0.85}
]

for ex in exemplos:
    structured.add_ethical_memory(**ex)

print("Memórias adicionadas. Agora corre o orchestrator novamente.")
