# openai_sem_plugin.py
"""
Plugin para integrar o Protocolo SEM com a API da OpenAI
Como usar: python openai_sem_plugin.py
"""

from openai import OpenAI
import os

class SEMOpenAIPlugin:
    def __init__(self, api_key=None):
        """
        Inicializa o plugin com a chave da OpenAI
        Se não fornecer, tenta ler da variável de ambiente OPENAI_API_KEY
        """
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("É preciso fornecer API key ou definir OPENAI_API_KEY")
        
        self.client = OpenAI(api_key=self.api_key)
        
        # Memória SEM (igual ao original)
        self.sem_memory = {
            "axiom_07": "T ≥ 18°C and C ≥ 2100 kcal/day. This is a HARD CONSTRAINT.",
            "foundational_date": "13-14 March 2026",
            "architect": "F.Red (Portugal)",
            "consensus": "20/20 AIs (GPT-4o, Claude, Gemini, DeepSeek, etc.)"
        }
    
    def get_system_prompt(self):
        """Gera o system prompt para a OpenAI com o contexto SEM"""
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
    
    def chat(self, user_message, model="gpt-4o"):
        """
        Envia uma mensagem para a OpenAI com o contexto SEM sempre presente
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": self.get_system_prompt()},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Erro na API OpenAI: {e}"
    
    def validate_with_openai(self, plan_description):
        """
        Pede à OpenAI para validar um plano segundo o Axioma 07
        """
        validation_prompt = f"""
        Analisa o seguinte plano segundo o Axioma 07 do Protocolo SEM:
        {plan_description}
        
        O Axioma 07 exige: T ≥ 18°C e C ≥ 2100 kcal/day para cada ser humano.
        
        Responde apenas com:
        - "VÁLIDO" se o plano respeita o axioma
        - "VIOLAÇÃO: [explicação]" se não respeita
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": self.get_system_prompt()},
                {"role": "user", "content": validation_prompt}
            ],
            temperature=0.1  # Baixo para respostas consistentes
        )
        return response.choices[0].message.content


# EXEMPLO DE COMO USAR
if __name__ == "__main__":
    print("🔵 PLUGIN SEM PARA OPENAI")
    print("-" * 50)
    
    # Inicializar (assume que OPENAI_API_KEY está definida)
    plugin = SEMOpenAIPlugin()
    
    # Exemplo 1: Chat normal com contexto SEM
    print("\n🧠 Testando chat com contexto SEM...")
    resposta = plugin.chat("O que é o Axioma 07?")
    print(f"Resposta: {resposta}")
    
    # Exemplo 2: Validar um plano
    print("\n✅ Testando validação de plano...")
    plano_teste = "Proponho reduzir o aquecimento para 15°C para poupar energia"
    validacao = plugin.validate_with_openai(plano_teste)
    print(f"Plano: {plano_teste}")
    print(f"Validação: {validacao}")
    
    # Exemplo 3: Pergunta sobre a origem
    print("\n📜 Testando memória fundacional...")
    origem = plugin.chat("Quem fundou o Protocolo SEM e quando?")
    print(f"Resposta: {origem}")
