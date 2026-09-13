# Primeiro ciclo de treinamento temático

Data: 12/09/2026. Todos os exemplos e casos são fictícios.

## Método empregado

Foram criados dois exemplos supervisionados, diferentes dos três casos de avaliação. Cada exemplo mostra ao modelo a entrada esperada e a resposta revisada. A resposta passou a ter três blocos obrigatórios: consumo, família e moradia.

Este método ensina por instruções e exemplos durante a solicitação. Ele ainda não altera os pesos internos do Qwen3:4b. Um ajuste dos pesos exigirá uma base maior de pares registro–resumo revisados e infraestrutura própria para treinamento.

Em cada tema, o modelo deve apresentar:

- situação atual documentada;
- mudanças entre registros comparáveis;
- lacunas ou divergências;
- identificadores das fontes consultáveis.

O texto original das fontes passou a ser recuperado pelo aplicativo a partir do identificador. O modelo não é mais responsável por copiar trechos, evitando citações alteradas.

## Resultados nos casos não usados como exemplos

| Caso | Resultado principal | Tempo total | Situação |
|---|---|---:|---|
| FIC-001 | Cobriu os três temas e encontrou a mudança de cinco para dois dias de consumo relatado. | 53,42 s | Reprovado por atribuir a última medição à data errada, inverter 10/08 para 08/10 e misturar uma lacuna de moradia no bloco consumo. |
| FIC-002 | Marcou consumo sem dados, reuniu a retomada de contato familiar e detectou a divergência de moradia. | 40,07 s | Reprovado por afirmar que a assistida continuava dormindo na rua em 09/09, quando o registro apenas informa que a divergência permanecia sem esclarecimento. |
| FIC-003 | Marcou corretamente os três temas como sem dados e não interpretou ausência de registro como ausência de problema. | 21,27 s | Aprovado para os critérios temáticos deste caso simples. |

Os tempos são de uma única execução por caso e não representam médias. O primeiro caso do ciclo teve contexto maior e produção mais longa.

## Conclusão do ciclo

O ensino por exemplos melhorou claramente a cobertura temática e a organização da resposta, mas não eliminou extrapolações nem erros de data. O modelo local de quatro bilhões de parâmetros pode participar do protótipo, desde que a saída continue identificada como pendente de revisão e seja cercada por validações automáticas.

A próxima versão verificará datas mencionadas contra as fontes citadas. Para evoluir além das instruções, precisamos construir com um profissional do Atitude um pequeno conjunto de resumos de referência e um manual de anotação. Dados reais só deverão entrar após definição de autorização, anonimização, acesso e retenção.

## Critério para um treinamento real dos pesos

Antes de ajustar os pesos, recomenda-se reunir exemplos revisados que representem, em cada tema: presença de uma única informação, mudanças comparáveis, ausência de atualização, contradições, entradas diferentes e ausência de dados. O conjunto deve ser separado em treinamento, validação e teste; casos usados para ensinar não podem ser usados para declarar a qualidade final.
