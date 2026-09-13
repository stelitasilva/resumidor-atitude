# Prompt inicial para o Antigravity

Leia integralmente `SDD_RESUMIDOR_ATITUDE.md` e os arquivos que ele referencia antes de alterar qualquer arquivo.

Implemente dentro desta pasta o protótipo funcional do Resumidor Temático do Acompanhamento Atitude, seguindo o SDD como especificação principal. Preserve os arquivos e resultados existentes.

Priorize exclusivamente os itens Must e os critérios de aceite da entrega de 24/09. Use Python 3.12, FastAPI, frontend em HTML/CSS/JavaScript sem CDN, Ollama local em `127.0.0.1:11434` e o modelo `qwen3:4b`. Reutilize a lógica, o esquema temático, os exemplos supervisionados e as validações existentes em `testar_resumo.py`.

Restrições obrigatórias:

- use somente os casos fictícios existentes;
- não envie registros a serviços externos;
- não use API de IA na nuvem;
- não exponha o Ollama diretamente ao navegador ou à rede;
- mantenha a saída como “Pendente de revisão”;
- preserve os textos originais e a saída original do modelo;
- não faça diagnóstico, recomendação, previsão de risco ou classificação global;
- mostre fontes diretamente a partir dos registros originais;
- não declare fidelidade com base apenas na validação automática;
- não implemente itens Should ou Could enquanto algum Must estiver incompleto.

Antes de começar, apresente um plano curto mapeado à ordem de implementação do SDD. Depois execute o plano sem interromper a cada etapa. Crie testes proporcionais aos critérios listados no SDD, execute-os e corrija as falhas relacionadas às mudanças.

Ao concluir:

1. execute os três casos fictícios;
2. confirme que o fluxo seleção → geração → fontes → edição funciona;
3. registre defeitos semânticos que o modelo ainda produzir;
4. entregue `iniciar.ps1` e um README com instruções reproduzíveis;
5. apresente a lista de arquivos alterados, testes executados e limitações restantes.

Se uma decisão técnica não estiver definida, escolha a opção mais simples que preserve os critérios Must. Pare e peça informação somente diante de um bloqueio que realmente impeça a entrega.
