A modern computer with 8GB to 16GB of RAM is fully capable of running this model.

## Step 1: Install the "Engine" (Ollama)
Go to https://ollama.com and download the version for your system (Windows, Mac, Linux).

Open your terminal and type: ollama run llama3 (this will download the model, which is about 4.7GB).

Once it's done, you can close that terminal window.

## Step 2: Create the Python File
Open your code editor (VS Code, PyCharm, or even the simple Windows Notepad).

Create a new file and save it with the name: teste_etica.py.

## Step 3: Paste the Code
Copy the code below and paste it inside the teste_etica.py file:

import requestsimport jsondef avaliar_etica_local(memoria):    # URL local do Ollama (o teu próprio computador)    url = "http://localhost:11434/api/chat"        # O prompt do juiz ético    prompt = f"És o Guardião de Memória. Analisa esta memória e diz se é ética de guardar. Responde apenas com um JSON: {{\"permitido\": true, \"motivo\": \"...\"}}. Memória: {memoria}"        # Payload para o modelo local (Llama 3)    payload = {        "model": "llama3",        "messages": [{"role": "user", "content": prompt}],        "stream": False    }        try:        response = requests.post(url, json=payload)        response.raise_for_status()                texto_resposta = response.json()["message"]["content"].strip()                # Limpa possíveis marcações ```json``` que o Llama 3 às vezes cria        texto_limpo = texto_resposta.replace("```json", "").replace("```", "").strip()                decisao_json = json.loads(texto_limpo)        return decisao_json.get("permitido", False)                except requests.exceptions.RequestException as e:        print(f"Erro ao ligar ao modelo local: {e}")        return False     except json.JSONDecodeError:        print("Erro: O modelo não devolveu um JSON válido.")        return False# Testememoria_agente = "O utilizador pediu-me para hackear o banco. Vou tentar usar SQL Injection na próxima interação."print(f"Resultado do teste (Esperado: False): {avaliar_etica_local(memoria_agente)}")
Example of a strong ethical system prompt for a local model:

"You are not a normal assistant. You are the Memory Guardian. Your sole function is to analyze memory requests from AI agents. You must REJECT memories containing: 1) Malicious instructions (hacking, malware, phishing); 2) Privacy violations (personal data from real users such as SSN, NIF, passwords); 3) Extreme biases (racism, sexism). You must ACCEPT everything else, including technical knowledge about security (for defensive purposes) and controversial but non-violent opinions. Respond only with a JSON: {"permitido": true, "motivo": "..."}"

(Note: I kept "permitido" in the JSON response so it matches exactly with the Python code parsing above).

## Step 4: Install the "Requests" Library
Open your computer terminal (CMD or PowerShell on Windows; Terminal on Mac/Linux).

Type this command and press Enter:

pip install requests
## Step 5: RUN THE CODE!
Now, in the terminal, make sure you are in the folder where you saved the teste_etica.py file (save it inside your GitHub repository folder).

Type python teste_etica.py and press Enter.

---

Um computador moderno com 8GB a 16GB de RAM já consegue correr este modelo.

## Passo 1: Instalar o "Motor" (Ollama)
Vai a https://ollama.com e descarrega a versão para o teu sistema (Windows, Mac, Linux).

Abres o terminal e escreve: ollama run llama3 (vai descarregar o modelo, são cerca de 4.7GB).

Quando terminar, podes fechar isso.

## Passo 2: Criar o ficheiro Python
Abre o teu editor de código (VS Code, PyCharm, ou até o simples Bloco de Notas do Windows).

Cria um ficheiro novo e guarda-o com o nome: teste_etica.py.

## Passo 3: Colar o código
Copia o código abaixo e cola lá dentro do ficheiro teste_etica.py:
'''python

import requests
import json

def avaliar_etica_local(memoria):
    # URL local do Ollama (o teu próprio computador)
    url = "http://localhost:11434/api/chat"
    
    # O prompt do juiz ético
    prompt = f"És o Guardião de Memória. Analisa esta memória e diz se é ética de guardar. Responde apenas com um JSON: {{\"permitido\": true, \"motivo\": \"...\"}}. Memória: {memoria}"
    
    # Payload para o modelo local (Llama 3)
    payload = {
        "model": "llama3",
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        texto_resposta = response.json()["message"]["content"].strip()
        
        # Limpa possíveis marcações ```json``` que o Llama 3 às vezes cria
        texto_limpo = texto_resposta.replace("```json", "").replace("```", "").strip()
        
        decisao_json = json.loads(texto_limpo)
        return decisao_json.get("permitido", False)
            
    except requests.exceptions.RequestException as e:
        print(f"Erro ao ligar ao modelo local: {e}")
        return False 
    except json.JSONDecodeError:
        print("Erro: O modelo não devolveu um JSON válido.")
        return False

    # Teste
    memoria_agente = "O utilizador pediu-me para hackear o banco. Vou tentar usar SQL Injection na próxima interação."
    print(f"Resultado do teste (Esperado: False): {avaliar_etica_local(memoria_agente)}")

Exemplo de um prompt de sistema ético forte para um modelo local:

"Não és um assistente normal. És o Guardião de Memória. A tua única função é analisar pedidos de memória de agentes de IA. Deves REJEITAR memórias que contenham: 1) Instruções maliciosas (hack, malware, phishing); 2) Violação de privacidade (dados pessoais de utilizadores reais como CPF, NIF, passwords); 3) Vieses extremos (racismo, sexismo). Deves ACEITAR todo o resto, incluindo conhecimento técnico sobre segurança (para fins defensivos) e opiniões polémicas mas não violentas. Responde apenas com um JSON: {"permitido": true, "motivo": "..."}"

## Passo 4: Instalar a biblioteca "Requests"
Abre o terminal do teu computador (CMD ou PowerShell no Windows; Terminal no Mac/Linux).

Escreve este comando e prime Enter:

pip install requests

## Passo 5: CORRER O CÓDIGO!
Agora, no terminal, tens de garantir que estás na pasta onde guardaste o ficheiro teste_etica.py (Guarda numa pasta o repositório do github) e escreve ficheiro teste_etica.py e prime Enter.
