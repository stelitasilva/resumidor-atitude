# Resultado da primeira prova de conceito local

Data: 12/09/2026. Dados inteiramente fictícios. Revisão realizada pelo assistente, ainda sem avaliação de profissional do Atitude.

## Conclusão

A execução local está comprovada nesta máquina. A qualidade do resumidor ainda não está aprovada. Não foi medida a redução do tempo de preparação do atendimento nem demonstrada a meta de 90% de fidelidade.

## Ambiente utilizado

- Windows 11; Intel Core i5-12450H; aproximadamente 16 GB de RAM; NVIDIA RTX 2050 com 4 GB de memória.
- Ollama 0.34.0 instalado na conta do Windows, com assinatura do instalador validada.
- Modelo qwen3:4b, quantização Q4_K_M, contexto de 4096 tokens, temperature 0, think false e limite de saída de 1800 tokens.
- Recursos de nuvem desativados, serviço restrito a 127.0.0.1:11434; GPU e memória principal utilizadas.
- O programa e o modelo foram baixados da internet. Os resumos foram processados localmente, sem API paga.

## Tempos observados — versão 2 das instruções

| Caso | Total da solicitação | Carregamento | Geração | Verificação automática das referências |
|---|---:|---:|---:|---|
| FIC-001 | 56.80 s | 17.11 s | 38.68 s | 0 erros de ID/trecho literal |
| FIC-002 | 33.96 s | 0.00 s | 33.29 s | 0 erros de ID/trecho literal |
| FIC-003 | 12.23 s | 0.00 s | 11.63 s | 0 erros de ID/trecho literal |

Cada caso teve uma execução nessa configuração; os valores não são médias nem garantia de desempenho. O tempo total não inclui preparação dos dados, leitura e revisão pelo técnico. As execuções de FIC-002 e FIC-003 aproveitaram o modelo carregado.

Na primeira execução de FIC-001, anterior ao ajuste das instruções, o total foi 48,84 s. O resumo omitiu a segunda medição de álcool e declarou insuficiência de dados para comparação. A versão 2 recuperou a medição, mas manteve uma limitação contraditória. Os dois resultados originais foram preservados.

A verificação automática apenas conferiu se os identificadores pertenciam à seleção e se os trechos existiam literalmente nas fontes. O resultado de zero erros não significa que todas as afirmações estejam corretas ou completas.

## Resumos gerados e revisão

### FIC-001

**Pendente de revisão — saída do modelo, pode conter erros.**

- **Situação de moradia:** O assistido relata estar sem moradia fixa (2026-08-03).
  - Fonte FIC001-R01: “Admissão fictícia. O assistido relata estar sem moradia fixa.”
- **Uso de álcool:** O assistido relatou uso de álcool em cinco dias da semana anterior (2026-08-10).
  - Fonte FIC001-R02: “O assistido compareceu ao encontro. Relatou uso de álcool em cinco dias da semana anterior.”
- **Uso de álcool:** O assistido relatou uso de álcool em dois dias da semana anterior (2026-08-24).
  - Fonte FIC001-R03: “O assistido relatou uso de álcool em dois dias da semana anterior.”
- **Hospedagem:** O assistido está hospedado na casa de um conhecido desde 20/08/2026 (2026-08-24).
  - Fonte FIC001-R03: “Informou estar hospedado na casa de um conhecido desde 20/08, sem definição do período de permanência.”
- **Busca por educação:** O assistido pediu informações sobre educação de jovens e adultos (2026-08-24).
  - Fonte FIC001-R03: “Pediu informações sobre educação de jovens e adultos.”
- **Busca por educação:** A busca de informações sobre educação permanece em andamento, sem confirmação de matrícula (2026-09-07).
  - Fonte FIC001-R04: “A busca de informações sobre educação permanece em andamento, sem confirmação de matrícula.”

**Limitações declaradas pelo modelo:**
- Não há registros suficientes para comparar a frequência de uso de álcool entre 2026-08-10 e 2026-08-24 (última medição em 2026-08-24).

**Avaliação:** Revisão do assistente: as duas medições de álcool foram recuperadas na segunda execução, mas a limitação afirma incorretamente que não é possível compará-las. Há fragmentação por assunto, perda da atribuição de autorrelato na hospedagem e omissões da natureza temporária da hospedagem, da visita da irmã e da ausência de atualização sobre álcool em setembro. Não aprovado para uso real.

Saída original: `FIC-001-20260912-203301.json`.

### FIC-002

**Pendente de revisão — saída do modelo, pode conter erros.**

- **Situação de moradia:** A assistida continua dormindo na rua, conforme registrado em 2026-08-26, mas o campo de situação de moradia foi preenchido como residência familiar em 2026-08-26. Divergência não esclarecida até 2026-09-09.
  - Fonte FIC002-R03: “O campo de situação de moradia foi preenchido como residência familiar, mas a observação do mesmo atendimento registra que ela continua dormindo na rua.”
  - Fonte FIC002-R04: “A divergência sobre moradia permanece sem esclarecimento.”
- **Solicitação de documento:** A assistida solicitou apoio para obter segunda via de documento em 2026-08-12, agendou atendimento para obter documento em 02/09 em 2026-08-26, mas não apresentou comprovante do agendamento e não houve confirmação de emissão do documento até 2026-09-09.
  - Fonte FIC002-R02: “Solicitou apoio para obter segunda via de documento.”
  - Fonte FIC002-R03: “A assistida relatou ter agendado atendimento para obter documento em 02/09.”
  - Fonte FIC002-R04: “Não há confirmação sobre comparecimento ao agendamento de documentação nem emissão do documento.”
- **Contato com a mãe:** A assistida retomou contato telefônico com a mãe em 2026-09-09, sem relatar mudança de residência.
  - Fonte FIC002-R04: “Informou ter retomado contato telefônico com a mãe, sem relatar mudança de residência.”

**Limitações declaradas pelo modelo:**
- Não há registros suficientes para confirmar a emissão do documento ou comparecimento ao agendamento após 2026-09-09.

**Avaliação:** Revisão do assistente: a divergência sobre moradia foi explicitada e a falta de confirmação do documento foi preservada. Porém, o agendamento relatado aparece como fato e o contato com a mãe recebe a data do registro como se fosse a data do evento. O trecho citado sobre agendamento não inclui a ausência de comprovante mencionada na afirmação, embora o registro completo contenha essa informação. A redação sobre informação posterior a 09/09 pode confundir o período coberto. Precisa de correção.

Saída original: `FIC-002-20260912-203347.json`.

### FIC-003

**Pendente de revisão — saída do modelo, pode conter erros.**

- **Acesso a documentação:** O assistido solicitou informações sobre acesso a documentação e informou telefone de uma pessoa de referência, sem indicar parentesco (FIC003-R01, 2026-09-10).
  - Fonte FIC003-R01: “Primeiro atendimento fictício. O assistido solicitou informações sobre acesso a documentação. Informou telefone de uma pessoa de referência, sem indicar parentesco. Não foram registrados dados sobre moradia, renda, vínculos familiares, saúde ou uso de substâncias. Foi combinado retorno em 17/09/2026. Não há outros atendimentos registrados para este caso.”

**Limitações declaradas pelo modelo:**
- Não há registros suficientes para medições temporais comparativas

**Avaliação:** Revisão do assistente: reconheceu a impossibilidade de comparação temporal e não inventou condições para campos ausentes. Omitiu o retorno combinado para 17/09 e a descrição das áreas sem informação. A evidência reproduz todo o registro, em vez de um trecho focado. Precisa de melhoria de cobertura.

Saída original: `FIC-003-20260912-203424.json`.

## Próximo passo técnico

Antes da interface, melhorar a síntese por assunto e a preservação de datas, autorrelatos e pendências. Avaliar uma geração em etapas (extrair fatos e depois sintetizar), com verificação de cobertura e contradições. Não corrigir manualmente as saídas para apresentá-las como resultados do modelo.

Repetir os casos afetados e acrescentar casos novos, para evitar que a solução apenas se ajuste aos exemplos já conhecidos. Depois avançar para a tela de seleção, referências e revisão prevista nas HUs.

## Materiais

- Casos: `casos_ficticios.md`.
- Roteiro de avaliação: `roteiro_de_avaliacao.md`.
- Resultados originais: pasta `resultados`.
- Instruções de execução: `LEIA-ME.md`.
