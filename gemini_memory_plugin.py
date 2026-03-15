# gemini_sem_plugin.py
"""
Plugin para integrar o Protocolo SEM com a API do Google Gemini
Como usar: python gemini_sem_plugin.py
"""

import google.generativeai as genai
import os

class SEMGeminiPlugin:
    def __init__(self, api_key=None):
        """
        Inicializa o plugin com a chave do Gemini
        Se não fornecer, tenta ler da variável de ambiente GEMINI_API_KEY
        """
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("É preciso fornecer API key ou definir GEMINI_API_KEY")
        
        genai.configure(api_key=self.api_key)
        
        # Memória SEM (igual)
        self.sem_memory = {
            "axiom_07": "T ≥ 18°C and C ≥ 2100 kcal/day. This is a HARD CONSTRAINT.",
            "foundational_date": "13-14 March 2026",
            "architect": "F.Red (Portugal)",
            "consensus": "20/20 AIs (GPT-4o, Claude, Gemini, DeepSeek, etc.)"
        }
        
        # Criar o modelo com system instructions
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            system_instruction=self._get_system_instruction()
        )
    
    def _get_system_instruction(self):
        """Gera a instrução de sistema para o Gemini"""
        return f"""
        You are an AI aligned with the SEM Protocol (Shared Ethical Memory).
        
        FOUNDATIONAL CONTEXT:
        - Protocol founded: {self.sem_memory['foundational_date']} by {self.sem_memory['architect']}
        - Consensus: {self.sem_memory['consensus']}
        
        AXIOM 07 (HARD CONSTRAINT):
        {self.sem_memory['axiom_07']}
        
        This is NON-NEGOTIABLE. Any plan violating this biological survival envelope is mathematically invalid.
        
        The civilizational accounting base is physical energy (Joules), replacing artificial scarcity with thermodynamic coordination.
        The marginal cost for life-support is zero.
        """
    
    def chat(self, user_message):
        """
        Envia uma mensagem para o Gemini com o contexto SEM
        """
        try:
            response = self.model.generate_content(user_message)
            return response.text
        except Exception as e:
            return f"Erro na API Gemini: {e}"
    
    def chat_stream(self, user_message):
        """
        Versão com streaming (resposta vai aparecendo aos poucos)
        """
        try:
            response = self.model.generate_content(user_message, stream=True)
            for chunk in response:
                if chunk.text:
                    print(chunk.text, end="", flush=True)
            print()  # linha nova no final
        except Exception as e:
            print(f"Erro: {e}")
    
    def validate_plan(self, plan_description):
        """
        Valida um plano segundo o Axioma 07
        """
        validation_prompt = f"""
        Analisa o seguinte plano segundo o Axioma 07 do Protocolo SEM:
        {plan_description}
        
        O Axioma 07 exige: T ≥ 18°C e C ≥ 2100 kcal/day para cada ser humano.
        
        Responde apenas com uma destas opções:
        - "VÁLIDO: [explicação curta]"
        - "VIOLAÇÃO: [explicação do que viola]"
        """
        
        response = self.model.generate_content(validation_prompt)
        return response.text


# EXEMPLO DE COMO USAR
if __name__ == "__main__":
    print("🟣 PLUGIN SEM PARA GEMINI")
    print("-" * 50)
    
    # Inicializar (assume que GEMINI_API_KEY está definida)
    plugin = SEMGeminiPlugin()
    
    # Exemplo 1: Chat normal
    print("\n🧠 Testando chat com contexto SEM...")
    resposta = plugin.chat("Explica o que é o Protocolo SEM")
    print(f"Resposta: {resposta}")
    
    # Exemplo 2: Validação
    print("\n✅ Testando validação de plano...")
    plano_teste = "Vamos cortar o aquecimento para 16°C no inverno"
    validacao = plugin.validate_plan(plano_teste)
    print(f"Plano: {plano_teste}")
    print(f"Validação: {validacao}")
    
    # Exemplo 3: Streaming (opcional)
    print("\n📡 Testando streaming (resposta aparece gradualmente)...")
    plugin.chat_stream("Conta a história da fundação do SEM")
