# Prova de conceito local — Resumidor Atitude

Esta pasta contém os primeiros insumos de teste. Ainda não é a interface funcional prevista para 24/09.

## Arquivos

- `casos_ficticios.md`: leitura dos três casos e seus nove registros.
- `dados/casos_ficticios.json`: os mesmos casos em formato de entrada para o programa.
- `roteiro_de_avaliacao.md`: fatos esperados, armadilhas e critérios de conferência.
- `dados/exemplos_treinamento.json`: exemplos fictícios revisados que ensinam o formato temático.
- `testar_resumo.py`: geração de resumo temático pela API local e validação de estrutura, fontes e datas citadas.
- `resultado_treinamento_temas.md`: avaliação do primeiro ciclo de ensino por exemplos.
- `resultados/`: resultados de execuções reais, quando realizadas, com tempos medidos.

## Execução

Requer Python 3 e Ollama executando em `127.0.0.1:11434`, com o modelo `qwen3:4b` previamente baixado. O programa usa apenas bibliotecas padrão do Python.

```powershell
python testar_resumo.py --caso FIC-001
python testar_resumo.py --caso FIC-002
python testar_resumo.py --caso FIC-003
```

O primeiro carregamento pode ser mais lento. O registro de tempo diferencia carga e geração, e o tempo total inclui toda a solicitação. Isso não equivale ao tempo de preparação do atendimento, que inclui revisão pelo técnico.

O programa seleciona somente os registros da entrada indicada no caso. No FIC-002, o registro da entrada antiga permanece na base de teste, mas não é enviado ao resumidor.

O texto de origem é dado, não instrução. O resumo deve estar pendente de revisão. A validação automática procura fontes fora da seleção e trechos inexistentes; não comprova por si só a correção das afirmações.

## Operação local

O aplicativo faz requisições somente ao endereço local. O download inicial do programa e do modelo requer internet. Executar o Ollama com recursos de nuvem desativados e sem exposição à rede externa. A implantação institucional e a interface para o técnico serão trabalhos posteriores.

Não inserir dados reais nesta fase. As referências e os critérios dos casos são exclusivamente para desenvolvimento; a avaliação acadêmica final usará outra amostra autorizada.
