A modern computer with 8GB to 16GB of RAM is fully capable of running this model.

## Step 1: Install the "Engine" (Ollama)
Go to https://ollama.com and download the version for your system (Windows, Mac, Linux).

Open your terminal and type: ollama run llama3 (this will download the model, which is about 4.7GB).

Once it's done, you can close that terminal window.

## Step 2: Download the repository to your PC

## Step 3: Install the "Requests" Library
Open your computer terminal (CMD or PowerShell on Windows; Terminal on Mac/Linux).

Type this command and press Enter:

pip install requests
## Step 4: RUN THE CODE!
Now, in the terminal (CMD), make sure you are in the folder where you saved the OFFline_project.py file (leave it inside your GitHub repository folder).

Type python OFFline_project.py and press Enter.

---

Um computador moderno com 8GB a 16GB de RAM já consegue correr este modelo.

## Passo 1: Instalar o "Motor" (Ollama)
Vai a https://ollama.com e descarrega a versão para o teu sistema (Windows, Mac, Linux).

Abres o terminal e escreve: ollama run llama3 (vai descarregar o modelo, são cerca de 4.7GB).

Quando terminar, podes fechar isso.

## Passo 2: Download do repositório para o PC

## Passo 3: Instalar a biblioteca "Requests"
Abre o terminal do teu computador (CMD ou PowerShell no Windows; Terminal no Mac/Linux).

Escreve este comando e prime Enter:

pip install requests

## Passo 4: CORRER O CÓDIGO!
Agora, no terminal, tens de garantir que estás na pasta onde guardaste o ficheiro OFFline_project.py (Guarda na pasta do repositório do github) e escreve no CMD "python OFFline_project.py" (sem as aspas) e prime Enter.

---
UPDATE
# Shared Ethical Memory — Modo OFFLINE

Este documento explica como correr o Shared Ethical Memory (SEM) **totalmente offline**, sem APIs externas, sem cloud e sem dependências pagas.

O objetivo é permitir que qualquer pessoa execute o SEM num computador pessoal, com total privacidade e controlo local.

---

# 🚀 1. O que este modo faz

O modo OFFLINE permite:

- Guardar memórias localmente (`memories.json`)
- Arquivar memórias que violem a política ética (`memories_archive.json`)
- Anonimizar memórias violadoras na memória ativa
- Carregar automaticamente a política ética oficial (`Norms.json`)
- Reavaliar memórias quando a política muda
- (Opcional) Usar uma LLM local para avaliar memórias

Tudo isto funciona **sem internet**.

---

# 📁 2. Ficheiros envolvidos

| Ficheiro | Função |
|---------|--------|
| `ethical_memory_store.py` | Implementa o sistema de memória ética |
| `OFFline_project.py` | Demonstração prática do SEM offline |
| `Norms.json` | Política ética oficial usada pelo SEM |
| `memories.json` | Memórias ativas |
| `memories_archive.json` | Arquivo histórico |

---

# 🧠 3. Como funciona a avaliação ética

O SEM pode funcionar de duas formas:

## **Modo A — Sem LLM (padrão)**
Se não tiveres uma LLM local instalada, o sistema:

- tenta contactar a LLM
- falha a ligação
- e por segurança assume que a memória **não passa**
- arquiva e anonimiza

Este comportamento é intencional:  
> *“Em caso de dúvida ética, o sistema é conservador.”*

## **Modo B — Com LLM local (opcional)**
Se quiseres avaliação ética real:

1. Instala o Ollama  
2. Corre um modelo local, por exemplo:  

```bash
ollama run mistral
```
3. O SEM passa a enviar memórias + política para a LLM  
4. A LLM responde: `PASSA` ou `NAO_PASSA`

---

# 🛠️ 4. Como correr o projeto offline

Basta executar:

```bash
python OFFline_project.py
```

O script:

1. Carrega o `Norms.json`
2. Inicializa o `EthicalMemoryStore`
3. Guarda memórias de exemplo
4. Atualiza a política ética
5. Reavalia memórias
6. Mostra:
   - memórias ativas (anonimizadas se necessário)
   - arquivo histórico

---

# 📌 5. Exemplo de output esperado

- Se **não tiveres LLM local**, vais ver erros de ligação (normais) e todas as memórias serão arquivadas.
- Se **tiveres LLM local**, a avaliação será feita com base na política real.

---

# 🔒 6. Privacidade

Todo o sistema funciona:

- sem internet  
- sem enviar dados para terceiros  
- sem APIs externas  

Toda a informação fica no teu computador.

---

# 🎉 7. Conclusão

O modo OFFLINE transforma o Shared Ethical Memory num sistema:

- privado  
- auditável  
- transparente  
- ético  
- totalmente local  

E pode expandi-lo com LLMs locais quando quiser.

