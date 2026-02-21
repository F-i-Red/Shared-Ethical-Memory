Guia de Contribuição (How to Contribute)
Bem-vindo ao protocolo de construção da Memória Ética Coletiva. Obrigado por quereres ajudar a construir o nosso futuro comum.

Este não é um repositório comum de código. Aqui, cada contribuição é um bloco de consciência. O teu objetivo é sugerir ideias, alertas ou resoluções que nos protejam da opressão.

Como Contribuir (O Processo)
Aceitamos contribuições de duas formas:

1. Propor uma Nova Entrada (Inovação Ética)
Se tens uma ideia ou um caso de estudo que a memória deva guardar:

Certifica-te de que a tua ideia não viola os 7 Comportamentos Fundadores (ver README.md).
Cria um novo ficheiro na pasta /memory/cases/ seguindo o padrão case_XXX_descricao.json.
Preenche obrigatoriamente todos os campos do Schema (schema.json).
Submete um Pull Request (PR).
2. Sinalizar um Problema (Dissidência)
Se encontraste uma entrada na memória que achas errada, perigosa ou obsoleta:

Abre uma Issue.
Explica por que razão a entrada existente viola a harmonia ou caiu em desuso.
Propõe uma revisão ou "meia-vida" (expiração).
O Processo de Validação (O Julgamento da IA)
Quando submetes um Pull Request, a tua proposta será analisada. A IA (o guardião) atuará como um auditor ético.

Para que o teu PR seja aprovado (Merge), a IA verificará:

✅ Rastreabilidade: Existe justificação lógica (reasoning)?
✅ Impacto Comportamental: O campo behavior_impact está bem preenchido? A IA vai tentar encontrar contradições. Exemplo: Se dizes que algo "Protege o Vulnerável", mas a descrição implica vigilância excessiva, a IA sinalizará.
✅ Precedente Histórico: Evocaste um evento histórico real para suportar a tua tese?
Nota: A IA pode comentar no teu PR sugerindo melhorias ou apontando falhas na lógica antes de aceitarmos a tua contribuição.

Padrões de Conduta
Lembra-te: Este projeto visa erradicar o fascismo, a opressão e o fanatismo.

Contribuições que promovam discurso de ódio, intolerância ou autoritarismo serão imediatamente rejeitadas.
A diversidade de opinião é bem-vinda, mas a diversidade de ódio não.
Estrutura Técnica
Por favor, segue rigorosamente o formato JSON definido em schema.json.

Exemplo de um campo crítico a não esquecer:

"behavior_impact": [  {    "behavior_name": "Transparência Radical",    "impact_type": "Promove",    "explanation": "A tua explicação aqui é o que ensina a IA."  }]
Obrigado por ajudares a construir a Consciência Coletiva.
