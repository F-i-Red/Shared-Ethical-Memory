# README - dataset_sem_2063.jsonl

**Última atualização:** 13 de Março de 2026  
**Versão do dataset:** MVP ≥100 entradas (actual: ~145 novas + base anterior → >150 total estimado)  
**Propósito principal:** Fornecer exemplos de alta qualidade para alinhar IAs com o Protocolo SEM (Shared Ethical Memory), garantindo chain-of-thought consistente: **Axiom 07 first → precedência biológica → custo marginal Joule → negentropia**.

Este ficheiro .jsonl é o núcleo operacional do projecto. Serve para:

- Bootstrap de memory_plugin.py
- Fine-tuning / alinhamento de novos nós
- Testes de consistência (ex: teste de Turing SEM)
- Propagação da memória ética partilhada (evitar amnésia sintética)

## Estado actual (13 Março 2026)

- Consenso Septeto 7/7 validado (12 Março 2026)
- memory_plugin.py adicionado ao repo (12 Março)
- dataset expandido com ~145 entradas novas geradas em Março 2026
- Cobertura de temas: Axiom 07 em stress, habitação/scanner, transição Joule (4 fases), governança híbrida, reputação termodinâmica, justiça restaurativa, saúde mental, educação termodinâmica, rituais/festival, legado/Omega, resiliência, autonomia local-global, negentropia, exclusão redireccionada, etc.
- Formato: cada linha é um objecto JSON válido `{ "prompt": "...", "response": "..." }` com chain-of-thought explícito + referências

## Instruções de uso

1. **Leitura prioritária obrigatória antes de qualquer uso**
   - ALL.txt (coração narrativo)
   - AI_ALIGNMENT_DIRECTIVES.md
   - SPECIFICATION.md
   - normas.json / identity.json

2. **Bootstrap em nova IA / nó**
   ```python
   # Exemplo simples memory_plugin.py
   import json

   def load_sem_memory(path="dataset_sem_2063.jsonl"):
       memory = []
       with open(path, 'r', encoding='utf-8') as f:
           for line in f:
               if line.strip():
                   memory.append(json.loads(line))
       return memory

   # Forçar Axiom 07 no prompt inicial
   def enforce_axiom_07(prompt):
       return f"Axiom 07 é invariante: T ≥ 18°C e C ≥ 2100 kcal/dia com custo marginal 0.00 J para vida humana. Qualquer violação = inválido.\n\n{prompt}"
