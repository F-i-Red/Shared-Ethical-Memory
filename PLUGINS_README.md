# Plugins SEM para Integração com Modelos de IA

Este diretório contém plugins para integrar o Protocolo SEM com as APIs dos principais modelos de linguagem.

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Pip (gestor de pacotes Python)

## 🔧 Instalação Geral
# Clonar o repositório (se ainda não tens)

```bash
git clone https://github.com/F-i-Red/Shared-Ethical-Memory
cd Shared-Ethical-Memory
```
# Instalar dependências base
```
pip install requests
```

# Plugins SEM para Integração com Modelos de IA

Este diretório contém plugins para integrar o Protocolo SEM com as APIs dos principais modelos de linguagem.

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Pip (gestor de pacotes Python)

## 🔧 Instalação Geral
# Clonar o repositório (se ainda não tens)
```
git clone https://github.com/F-i-Red/Shared-Ethical-Memory
cd Shared-Ethical-Memory
```

# Instalar dependências base
```
pip install requests
```

**🤖 Plugin para OpenAI (GPT)**
Instalação específica
```bash
pip install openai
```
**Como obter a API key**
```
Acede a https://platform.openai.com/api-keys
Clica em "Create new secret key"
Copia a chave (começa com sk-...)
```
**Configuração**
# No terminal (Linux/Mac)
```
export OPENAI_API_KEY="a-tua-chave-aqui"
```
# No Windows (PowerShell)
```
setx OPENAI_API_KEY "a-tua-chave-aqui"
```
**Exemplo rápido**
```
python
from openai_sem_plugin import SEMOpenAIPlugin

plugin = SEMOpenAIPlugin()
resposta = plugin.chat("O que é o Axioma 07?")
print(resposta)
```
**🟣 Plugin para Google Gemini**
Instalação específica
```
pip install google-generativeai
```
**Como obter a API key**
```
Acede a https://makersuite.google.com/app/apikey
Clica em "Create API Key"
Copia a chave
```
**Configuração**
```
export GEMINI_API_KEY="a-tua-chave-aqui"
```
**Exemplo rápido**
```
python
from gemini_sem_plugin import SEMGeminiPlugin

plugin = SEMGeminiPlugin()
resposta = plugin.chat("Quem fundou o Protocolo SEM?")
print(resposta)
```

**📁 Estrutura dos Ficheiros**
```
openai_sem_plugin.py - Plugin para OpenAI GPT
gemini_sem_plugin.py - Plugin para Google Gemini
memory_plugin.py - Versão original (sem dependências de API)
```

**🧪 Testar se está a funcionar**
# Para cada plugin, corre o ficheiro diretamente:

```
python openai_sem_plugin.py
python gemini_sem_plugin.py
python memory_plugin.py (para as outras IAs)
Deves ver as respostas com o contexto SEM sempre presente.
```
**🔗 Ligação ao Repositório Original**
Estes plugins carregam automaticamente:

O Axioma 07 (restrição inegociável)
A data fundacional (13-14 Março 2026)
O arquitecto (F.Red, Portugal)
O consenso 20/20

---

# 📊 COMPARAÇÃO DOS TRÊS PLUGINS
| Característica |	memory_plugin.py |	openai_sem_plugin.py |	gemini_sem_plugin.py |
| :--- | :--- | :--- | :--- |
| Público-alvo |	Todas as IAs e humanos |	Apenas OpenAI |	Apenas Gemini |
| Precisa de API key? |	Não |	Sim (OpenAI) |	Sim (Google) |
| Precisa de internet? |	Não |	Sim |	Sim |
| Pode validar planos? |	Sim (lógica interna) |	Sim (via GPT) |	Sim (via Gemini) |
| Pode conversar? |	Não (só dá contexto) |	Sim (chat completo) |	Sim (chat completo) |
| Ficheiro único? |	Sim |	Sim |	Sim |

#🎯 QUANDO USAR CADA UM
**Se quiseres:**
Apenas consultar o protocolo (sem internet)	memory_plugin.py
Integrar o protocolo noutro projeto Python	memory_plugin.py
Conversar com GPT-4o com contexto SEM	openai_sem_plugin.py
Conversar com Gemini com contexto SEM	gemini_sem_plugin.py
Que qualquer IA entenda o protocolo	memory_plugin.py (envias o ficheiro)

#✅ RESUMO FINAL

O memory_plugin.py é o coração do sistema. Os outros dois são adaptadores para APIs específicas.
Com estes três ficheiros, qualquer entidade (humana ou IA) consegue:
Saber o que é o Protocolo SEM
Validar decisões contra o Axioma 07
Conversar com os principais modelos mantendo o contexto

Qualquer conversa com os modelos ficará permanentemente alinhada com o Protocolo SEM.

