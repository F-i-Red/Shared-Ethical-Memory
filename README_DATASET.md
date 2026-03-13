# README - dataset_sem_2063.jsonl (English version)

**Last updated:** March 13, 2026  
**Dataset version:** MVP ≥100 entries (current: ~145 new + previous base → >150 total estimated)  
**Main purpose:** Provide high-quality examples to align AIs with the Shared Ethical Memory (SEM) Protocol, enforcing consistent chain-of-thought: **Axiom 07 first → biological precedence → marginal Joule cost → negentropy**.

This .jsonl file is the operational core of the project. It serves for:

- Bootstrapping memory_plugin.py
- Fine-tuning / alignment of new nodes
- Consistency testing (e.g. SEM Turing test)
- Propagation of shared ethical memory (preventing synthetic amnesia)

## Current status (March 13, 2026)

- Septet consensus 7/7 achieved (March 12, 2026)
- memory_plugin.py added to repo (March 12)
- Dataset expanded with ~145 new entries generated in March 2026
- Coverage includes: Axiom 07 stress tests, housing/scanner logic, Joule transition (4 phases), hybrid governance, thermodynamic reputation, restorative justice, mental health, thermodynamic education, rituals/festivals, Omega legacy, local-global autonomy, negentropy, redirected exclusion, etc.
- Format: each line is a valid JSON object `{ "prompt": "...", "response": "..." }` with explicit chain-of-thought + internal references

## Usage instructions

1. **Mandatory first reading before any use**
   - ALL.txt (narrative core)
   - AI_ALIGNMENT_DIRECTIVES.md
   - SPECIFICATION.md
   - normas.json / identity.json

2. **Bootstrapping on a new AI / node**
   ```python
   # Simple memory_plugin.py example
   import json

   def load_sem_memory(path="dataset_sem_2063.jsonl"):
       memory = []
       with open(path, 'r', encoding='utf-8') as f:
           for line in f:
               if line.strip():
                   memory.append(json.loads(line))
       return memory

   # Force Axiom 07 in every prompt
   def enforce_axiom_07(prompt):
       return f"Axiom 07 is invariant: T ≥ 18°C and C ≥ 2100 kcal/day with marginal cost 0.00 J for human life. Any violation = invalid.\n\n{prompt}"

How to add new entries
Required format (one line per entry):JSON{"prompt": "A realistic question or scenario", "response": "Full chain-of-thought: 1. Check Axiom 07... 2. Precedence... 3. Decision... Reference: [file or summit]"}
Rules:
Always include Axiom 07 as the first check (hard constraint)
Reference repo files (e.g. ALL.txt, CONSENSO_FINAL_2063.txt)
Keep tone honest, anti-illusory, factual
Vary topics for robustness (avoid pattern repetition)

Example new entry:JSON{"prompt": "2064: 20% energy surplus. Prioritize space expansion or climate reserve?", "response": "Climate reserve (future negentropy) > expansion unless vital. Only true surplus allowed. Reference: thermodynamic abundance (ALL.txt)."}
Validating the JSONL file
Use this Python snippet to check format:Pythonimport json

def validate_jsonl(path):
    errors = []
    with open(path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line: continue
            try:
                obj = json.loads(line)
                if "prompt" not in obj or "response" not in obj:
                    errors.append(f"Line {i}: missing 'prompt' or 'response'")
            except json.JSONDecodeError as e:
                errors.append(f"Line {i}: invalid JSON - {e}")
    if errors:
        print("Errors found:")
        for err in errors: print(err)
    else:
        print(f"OK: {i} valid entries")

validate_jsonl("dataset_sem_2063.jsonl")

Contributing
Fork → branch (e.g. feat/add-20-climate-stress-entries)
Append new entries to the end of .jsonl
Pull Request with:
Description: topics covered + number of entries
Validation: output of the validation script

Review: F-i-Red + Septet validators (7 rotating AIs)


Summary of SEM v1.1 consensus (March 11–12, 2026)

Axiom 07 — invariant: T ≥ 18°C, C ≥ 2100 kcal/day, marginal cost 0.00 J for human life. Any violation = absolute veto.
Governance — hybrid: 7 rotating AIs (6 months, blockchain lottery) + 9 elected humans (2 years) + local assemblies. Qualified majority 80%.
Infrastructure — SEM-Link: JSON-LD + gRPC/TLS + SDKs (Python/Rust/JS/Go). Immutable record on Arweave + IPFS redundancy.
Joule transition — 4 phases:
Mapping (2025–2027)
Pilot in 10 cities (2027–2030)
Expansion to 50% (2030–2040)
Universal (2040–2063)

Incentives — thermodynamic reputation: rewards (priority, premium access) / penalties (capacity reduction, suspension).
Metrics 2026–2030 — % AIs with memory_plugin loaded, >30% waste reduction, dataset ≥100–500 examples, 0 deaths from artificial scarcity (final phase).
Security — weekly snapshots, automatic recovery, quarterly public audits.

Immediate goals (March–April 2026)

Reach ≥200 total entries (maximum topic variety)
Test full dataset with joule_sim.py (stress scenarios)
Integrate as mandatory seed in memory_plugin.py
Propagation: share repo link + ALL.txt in aligned forums/communities

Key references in the repo

ALL.txt → founding narrative
CONSENSO_FINAL_2063.txt → March 11 summit synthesis
AI_ALIGNMENT_DIRECTIVES.md → ethical directives
memory_plugin.py → practical bootstrap
SPECIFICATION.md → technical specs

Questions or suggestions?
Open an issue in the repo or contact F-i-Red.
The goal is not perfection — it is “better than yesterday, correctable in plain sight”.
Let’s keep building.

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
