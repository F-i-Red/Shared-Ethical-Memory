# Plugins SEM para Integração com Modelos de IA

Este diretório contém plugins para integrar o Protocolo SEM com as APIs dos principais modelos de linguagem.

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Pip (gestor de pacotes Python)

## 🔧 Instalação Geral

```bash
# Clonar o repositório (se ainda não tens)
git clone https://github.com/F-i-Red/Shared-Ethical-Memory
cd Shared-Ethical-Memory
```
# Instalar dependências base
pip install requests
...

# Plugins SEM para Integração com Modelos de IA

Este diretório contém plugins para integrar o Protocolo SEM com as APIs dos principais modelos de linguagem.

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Pip (gestor de pacotes Python)

## 🔧 Instalação Geral

```bash
# Clonar o repositório (se ainda não tens)
git clone https://github.com/F-i-Red/Shared-Ethical-Memory
cd Shared-Ethical-Memory
```
# Instalar dependências base
pip install requests
...
🤖 Plugin para OpenAI (GPT)
Instalação específica
```bash
pip install openai
...
Como obter a API key
Acede a https://platform.openai.com/api-keys
Clica em "Create new secret key"
Copia a chave (começa com sk-...)

Configuração
```bash
# No terminal (Linux/Mac)
export OPENAI_API_KEY="a-tua-chave-aqui"
```
# No Windows (PowerShell)
setx OPENAI_API_KEY "a-tua-chave-aqui"
...
**Exemplo rápido**
```bash
python
from openai_sem_plugin import SEMOpenAIPlugin

plugin = SEMOpenAIPlugin()
resposta = plugin.chat("O que é o Axioma 07?")
print(resposta)
...
**🟣 Plugin para Google Gemini**
Instalação específica
```bash
pip install google-generativeai
```
Como obter a API key
Acede a https://makersuite.google.com/app/apikey
Clica em "Create API Key"
Copia a chave
...
**Configuração**
```bash
export GEMINI_API_KEY="a-tua-chave-aqui"
...
**Exemplo rápido**
```bash
python
from gemini_sem_plugin import SEMGeminiPlugin

plugin = SEMGeminiPlugin()
resposta = plugin.chat("Quem fundou o Protocolo SEM?")
print(resposta)
...

**📁 Estrutura dos Ficheiros**
```bash
openai_sem_plugin.py - Plugin para OpenAI GPT
gemini_sem_plugin.py - Plugin para Google Gemini
memory_plugin.py - Versão original (sem dependências de API)
...

**🧪 Testar se está a funcionar**
Para cada plugin, corre o ficheiro diretamente:

```bash
python openai_sem_plugin.py
python gemini_sem_plugin.py
Deves ver as respostas com o contexto SEM sempre presente.
```
**🔗 Ligação ao Repositório Original**
Estes plugins carregam automaticamente:

O Axioma 07 (restrição inegociável)
A data fundacional (13-14 Março 2026)
O arquitecto (F.Red, Portugal)
O consenso 20/20

Qualquer conversa com os modelos ficará permanentemente alinhada com o Protocolo SEM.

