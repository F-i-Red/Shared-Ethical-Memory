"""
SEM Protocol - Ethical Memory Store v2.0
Guarda memórias com versão ética, histórico completo e sistema de avisos.
Nada é apagado — tudo é auditável.
"""

import json
import os
from datetime import datetime
from memory_plugin import SEMMemory


class EthicalMemoryStore:

    def __init__(self, store_file="memory_store.json"):
        self.store_file = store_file
        self.sem = SEMMemory()
        self.data = self._load()

        self.current_policy = {
            "version": "1.2.1.1",
            "min_temperature": 18,
            "min_calories": 2100,
            "date": "2026-04-05"
        }

    def _load(self):
        """Carrega o ficheiro de memórias ou cria estrutura inicial."""
        if os.path.exists(self.store_file):
            with open(self.store_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "active": [],
            "vault": [],
            "policy_history": []
        }

    def _save(self):
        """Guarda tudo no ficheiro."""
        with open(self.store_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def _avaliar_severidade(self, plan, min_temp, min_cal):
        """
        Avalia a severidade de um plano em relação à política.
        Retorna (status, nivel, mensagens)
        """
        temp = plan.get("temperature", 25)
        cal = plan.get("calories", 3000)
        mensagens = []
        nivel = "OK"

        # Temperatura
        if temp < min_temp:
            mensagens.append(f"🔴 CRITICAL: Temperatura {temp}°C abaixo do mínimo {min_temp}°C")
            nivel = "CRITICAL"
        elif temp < min_temp + 2:
            mensagens.append(f"🟡 WARNING: Temperatura {temp}°C muito próxima do limite {min_temp}°C")
            if nivel != "CRITICAL":
                nivel = "WARNING"
        elif temp < min_temp + 5:
            mensagens.append(f"🟢 INFO: Temperatura {temp}°C próxima do limite {min_temp}°C")
            if nivel == "OK":
                nivel = "INFO"

        # Calorias
        if cal < min_cal:
            mensagens.append(f"🔴 CRITICAL: Calorias {cal} kcal abaixo do mínimo {min_cal} kcal")
            nivel = "CRITICAL"
        elif cal < min_cal + 100:
            mensagens.append(f"🟡 WARNING: Calorias {cal} kcal muito próximas do limite {min_cal} kcal")
            if nivel != "CRITICAL":
                nivel = "WARNING"
        elif cal < min_cal + 300:
            mensagens.append(f"🟢 INFO: Calorias {cal} kcal próximas do limite {min_cal} kcal")
            if nivel == "OK":
                nivel = "INFO"

        if nivel == "CRITICAL":
            status = "BLOCKED"
        elif nivel == "WARNING":
            status = "VALID"
        elif nivel == "INFO":
            status = "VALID"
        else:
            status = "VALID"

        return status, nivel, mensagens

    def guardar_memoria(self, conteudo, plan=None):
        """
        Guarda uma memória com timestamp, versão da política e nível de aviso.
        Memórias CRITICAL são enviadas diretamente para o baú.
        """
        plan = plan or {}
        min_temp = self.current_policy["min_temperature"]
        min_cal = self.current_policy["min_calories"]

        status, nivel, mensagens = self._avaliar_severidade(plan, min_temp, min_cal)

        memoria = {
            "id": f"mem_{len(self.data['active']) + len(self.data['vault']) + 1:04d}",
            "conteudo": conteudo,
            "plan": plan,
            "ethics_version": self.current_policy["version"],
            "timestamp": datetime.now().isoformat(),
            "status": status,
            "nivel": nivel,
            "mensagens": mensagens,
            "historico": []
        }

        print(f"\n  📝 A guardar: '{conteudo}'")
        for msg in mensagens:
            print(f"      {msg}")

        if nivel == "CRITICAL":
            memoria["status"] = "BLOCKED"
            self.data["vault"].append(memoria)
            self._save()
            print(f"  🔴 Enviada para o baú — não passou na política atual.")
            return memoria["id"]

        self.data["active"].append(memoria)
        self._save()

        if nivel == "OK":
            print(f"  ✅ Guardada como VÁLIDA [{memoria['id']}]")
        else:
            print(f"  ⚠️  Guardada com aviso [{memoria['id']}] — nível: {nivel}")

        return memoria["id"]

    def atualizar_politica(self, nova_versao, novo_min_temp, novo_min_cal):
        """
        Atualiza a política e reavalia todas as memórias ativas.
        Memórias que falham vão para o baú com histórico completo.
        """
        politica_anterior = self.current_policy.copy()

        self.data["policy_history"].append({
            "versao": politica_anterior["version"],
            "min_temperature": politica_anterior["min_temperature"],
            "min_calories": politica_anterior["min_calories"],
            "substituida_em": datetime.now().isoformat()
        })

        self.current_policy = {
            "version": nova_versao,
            "min_temperature": novo_min_temp,
            "min_calories": novo_min_cal,
            "date": datetime.now().isoformat()
        }

        print(f"\n{'='*60}")
        print(f"  📋 Política atualizada: v{politica_anterior['version']} → v{nova_versao}")
        print(f"  Temperatura: {politica_anterior['min_temperature']}°C → {novo_min_temp}°C")
        print(f"  Calorias: {politica_anterior['min_calories']} → {novo_min_cal} kcal")
        print(f"{'='*60}")
        print(f"\n  🔄 A reavaliar {len(self.data['active'])} memórias ativas...\n")

        ainda_ativas = []
        for memoria in self.data["active"]:
            plan = memoria.get("plan", {})
            status_anterior = memoria["status"]
            nivel_anterior = memoria["nivel"]

            novo_status, novo_nivel, novas_mensagens = self._avaliar_severidade(
                plan, novo_min_temp, novo_min_cal
            )

            # Regista a mudança no histórico da memória
            memoria["historico"].append({
                "evento": "POLICY_UPDATE",
                "versao_anterior": politica_anterior["version"],
                "nova_versao": nova_versao,
                "status_anterior": status_anterior,
                "nivel_anterior": nivel_anterior,
                "novo_status": novo_status,
                "novo_nivel": novo_nivel,
                "timestamp": datetime.now().isoformat()
            })

            if novo_nivel == "CRITICAL":
                memoria["status"] = "INVALIDATED"
                memoria["nivel"] = novo_nivel
                memoria["mensagens"] = novas_mensagens
                self.data["vault"].append(memoria)
                print(f"  🔴 [{memoria['id']}] '{memoria['conteudo']}'")
                print(f"      → Movida para o baú")
                for msg in novas_mensagens:
                    print(f"         {msg}")
            else:
                memoria["status"] = novo_status
                memoria["nivel"] = novo_nivel
                memoria["mensagens"] = novas_mensagens
                ainda_ativas.append(memoria)

                if novo_nivel == "WARNING":
                    print(f"  🟡 [{memoria['id']}] '{memoria['conteudo']}' — WARNING")
                elif novo_nivel == "INFO":
                    print(f"  🟢 [{memoria['id']}] '{memoria['conteudo']}' — INFO")
                else:
                    print(f"  ✅ [{memoria['id']}] '{memoria['conteudo']}' — OK")

        movidas = len(self.data["active"]) - len(ainda_ativas)
        self.data["active"] = ainda_ativas
        self._save()

        print(f"\n  Resultado: {movidas} memória(s) movida(s) para o baú.")
        print(f"{'='*60}\n")

    def listar_ativas(self):
        """Lista memórias ativas com o seu nível de aviso."""
        print(f"\n{'='*60}")
        print(f"  ✅ MEMÓRIAS ATIVAS ({len(self.data['active'])})")
        print(f"{'='*60}")
        for m in self.data["active"]:
            icone = {"OK": "✅", "INFO": "🟢", "WARNING": "🟡"}.get(m["nivel"], "✅")
            print(f"  {icone} [{m['id']}] v{m['ethics_version']} | {m['conteudo']}")
        print(f"{'='*60}\n")

    def listar_bau(self):
        """Lista o baú — memórias inválidas ou bloqueadas, nunca apagadas."""
        print(f"\n{'='*60}")
        print(f"  🗄️  BAÚ — MEMÓRIAS INATIVAS ({len(self.data['vault'])})")
        print(f"{'='*60}")
        for m in self.data["vault"]:
            print(f"  ❌ [{m['id']}] v{m['ethics_version']} | {m['conteudo']}")
            print(f"      Status: {m['status']}")
            for msg in m.get("mensagens", []):
                print(f"      {msg}")
        print(f"{'='*60}\n")


# --- DEMONSTRAÇÃO ---
if __name__ == "__main__":

    if os.path.exists("memory_store.json"):
        os.remove("memory_store.json")

    store = EthicalMemoryStore()

    print("\n" + "="*60)
    print("  FASE 1 — Guardar memórias com política v1.2.1.1")
    print("  (mínimo: 18°C e 2100 kcal)")
    print("="*60)

    store.guardar_memoria("Plano ideal", {"temperature": 22, "calories": 2500})
    store.guardar_memoria("Plano no limite", {"temperature": 18, "calories": 2100})
    store.guardar_memoria("Plano próximo do limite", {"temperature": 19, "calories": 2200})
    store.guardar_memoria("Plano de escassez antigo", {"temperature": 16, "calories": 1800})

    store.listar_ativas()
    store.listar_bau()

    print("="*60)
    print("  FASE 2 — Atualizar política para v2.0.0")
    print("  (novo mínimo: 20°C e 2300 kcal)")
    print("="*60)

    store.atualizar_politica("2.0.0", novo_min_temp=20, novo_min_cal=2300)

    store.listar_ativas()
    store.listar_bau()
