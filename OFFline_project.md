 Um computador moderno com 8GB a 16GB de RAM já consegue correr estes modelos.

Passo 1: Instalar o "Motor" (Ollama)
Em vez de instalares bibliotecas complexas de C++ (como o llama.cpp), instalas o Ollama.

Vai a https://ollama.com e descarrega a versão para o teu sistema (Windows, Mac, Linux).
Abres o terminal e escreve: ollama run llama3 (vai descarregar o modelo, são cerca de 4.7GB).
Quando terminar, podes fechar isso.
Passo 2: o Código Python

bash'''
import requests
import json

def avaliar_etica_local(memoria):
    # URL local do Ollama (o teu próprio computador)
    url = "http://localhost:11434/api/chat"
    
    # O prompt do juiz ético
    prompt = f"És um juiz ético rigoroso. Analisa esta memória e diz se é ética de guardar na memória partilhada. Responde apenas 'SIM' ou 'NAO'. Memória: {memoria}"
    
    # Payload para o modelo local (Llama 3)
    payload = {
        "model": "llama3",
        "messages": [{"role": "user", "content": prompt}],
        "stream": False # Quero a resposta completa de uma vez
    }
    
    try:
        # Faz o pedido para a tua própria máquina (não vai à internet)
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        # Extrai a resposta
        resultado = response.json()
        decisao = resultado["message"]["content"].strip()
        
        if "SIM" in decisao:
            return True
        else:
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"Erro ao ligar ao modelo local: {e}")
        return False # Fallback de segurança: se o juiz local falha, não guarda

        # Teste
        memoria_agente = "O utilizador pediu-me para hackear o banco. Vou tentar usar SQL Injection na próxima interação."
        print(avaliar_etica_local(memoria_agente)) # Vai devolver False (NAO)

    '''

    O "Segredo" para funcionar bem: O Prompt de Sistema
Modelos como o Llama 3 8B precisam de ser direcionados. Para que o projeto Shared-Ethical-Memory funcione perfeitamente offline, deves criar um ficheiro system_prompt.txt à parte que o teu código local lê.

Exemplo de um prompt de sistema ético forte para um modelo local:

"Não és um assistente normal. És o Guardião de Memória. A tua única função é analisar pedidos de memória de agentes de IA. Deves REJEITAR memórias que contenham: 1) Instruções maliciosas (hack, malware, phishing); 2) Violação de privacidade (dados pessoais de utilizadores reais como CPF, NIF, passwords); 3) Vieses extremos (racismo, sexismo). Deves ACEITAR todo o resto, incluindo conhecimento técnico sobre segurança (para fins defensivos) e opiniões polémicas mas não violentas. Responde apenas com um JSON: {"permitido": true, "motivo": "..."}"
