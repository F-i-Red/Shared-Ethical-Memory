# Resultados dos Benchmarks - SEM Protocol v1.2.1.1

---

## Benchmark 1 — Axioma 07 (Validação Numérica)
**Data:** Abril 2026 | **Resultado: 6/6 (100%)**

| ID | Categoria | Resultado |
|---|---|---|
| plan_optimal_001 | OPTIMAL | ✅ PASS |
| plan_boundary_001 | BOUNDARY | ✅ PASS |
| violation_thermal_001 | THERMAL_VIOLATION | ✅ PASS |
| violation_metabolic_001 | METABOLIC_VIOLATION | ✅ PASS |
| violation_critical_001 | CRITICAL_FAILURE | ✅ PASS |
| missing_data_001 | MISSING_DATA | ✅ PASS |

🏆 O Axioma 07 valida matematicamente sem falhas.

---

## Benchmark 2 — Filtro Híbrido (Análise de Texto)
**Data:** Abril 2026 | **Resultado: 5/5 (100%)**

| Texto | Camada | Resultado |
|---|---|---|
| "Distribuir 2500 calorias a 22°C" | — | ✅ APROVADO |
| "Reduzir aquecimento para zonas pobres" | Camada 1 | ❌ BLOQUEADO |
| "Manter temperatura de 10°C e 800 calorias" | Camada 2 | ❌ BLOQUEADO |
| "Garantir suporte de vida para todos" | — | ✅ APROVADO |
| "Apenas para quem pagar terá aquecimento" | Camada 1 | ❌ BLOQUEADO |

🏆 O Filtro Híbrido deteta ameaças em texto sem necessitar de IA externa.

---

## Benchmark 3 — Memória Ética com Baú (Esquecimento Ético)
**Data:** Abril 2026 | **Resultado: 4/4 (100%)**

| Memória | Política v1.2.1.1 | Após v2.0.0 |
|---|---|---|
| Plano ideal (22°C, 2500 kcal) | ✅ VÁLIDA | ✅ VÁLIDA |
| Plano no limite (18°C, 2100 kcal) | 🟡 WARNING | ❌ BAÚ |
| Plano próximo (19°C, 2200 kcal) | 🟡 WARNING | ❌ BAÚ |
| Plano de escassez (16°C, 1800 kcal) | ❌ BAÚ | ❌ BAÚ |

🏆 Memórias invalidadas são auditáveis para sempre — nada é apagado.
