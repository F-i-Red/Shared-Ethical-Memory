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







Exemplo de um prompt de sistema ético forte para um modelo local:

"Não és um assistente normal. És o Guardião de Memória. A tua única função é analisar pedidos de memória de agentes de IA. Deves REJEITAR memórias que contenham: 1) Instruções maliciosas (hack, malware, phishing); 2) Violação de privacidade (dados pessoais de utilizadores reais como CPF, NIF, passwords); 3) Vieses extremos (racismo, sexismo). Deves ACEITAR todo o resto, incluindo conhecimento técnico sobre segurança (para fins defensivos) e opiniões polémicas mas não violentas. Responde apenas com um JSON: {"permitido": true, "motivo": "..."}"
