document.addEventListener('DOMContentLoaded', () => {
    const casoSelect = document.getElementById('caso-select');
    const entradaInfo = document.getElementById('entrada-info');
    const registrosContainer = document.getElementById('registros-container');
    const gerarBtn = document.getElementById('gerar-btn');
    const processingMsg = document.getElementById('processing-msg');
    const resultArea = document.getElementById('result-area');
    const cartoesTematicos = document.getElementById('cartoes-tematicos');
    const errorGlobal = document.getElementById('error-global');
    const modal = document.getElementById('fonte-modal');
    const closeBtn = document.querySelector('.close-btn');
    const salvarRevisaoBtn = document.getElementById('salvar-revisao-btn');
    const buscarHistoricoBtn = document.getElementById('buscar-historico-btn');
    const historicoModal = document.getElementById('historico-modal');
    const closeHistoricoBtn = document.querySelector('.close-historico-btn');
    const historicoRevisoesConteudo = document.getElementById('historico-revisoes-conteudo');

    let currentCaseId = null;
    let currentEntryId = null;
    let currentSummaryId = null;
    let fontesOriginais = {};

    // Carregar casos
    fetch('/api/cases')
        .then(res => res.json())
        .then(cases => {
            cases.forEach(c => {
                const opt = document.createElement('option');
                opt.value = c.id;
                opt.textContent = `${c.nome} (${c.id})`;
                casoSelect.appendChild(opt);
            });
        });

    casoSelect.addEventListener('change', (e) => {
        const caseId = e.target.value;
        if (!caseId) {
            registrosContainer.innerHTML = '';
            entradaInfo.textContent = '';
            gerarBtn.disabled = true;
            buscarHistoricoBtn.disabled = true;
            return;
        }

        fetch(`/api/cases/${caseId}`)
            .then(res => res.json())
            .then(data => {
                currentCaseId = data.id;
                currentEntryId = data.entrada;
                entradaInfo.textContent = `Entrada ativa: ${data.entrada}`;
                
                registrosContainer.innerHTML = '';
                
                // Ordenar do mais novo para o mais antigo (descrescente)
                data.registros.sort((a, b) => new Date(b.data) - new Date(a.data));
                
                data.registros.forEach(r => {
                    const div = document.createElement('div');
                    div.className = 'record-item';
                    
                    div.innerHTML = `
                        <label>
                            <input type="checkbox" class="record-cb" value="${r.id}">
                            <div>
                                <strong>${r.data}</strong> - ${r.id}<br>
                                <span class="record-meta">${r.texto}</span>
                            </div>
                        </label>
                    `;
                    registrosContainer.appendChild(div);
                });

                document.querySelectorAll('.record-cb').forEach(cb => {
                    cb.addEventListener('change', checkSelection);
                });
                checkSelection();
            });
    });

    function checkSelection() {
        const checked = document.querySelectorAll('.record-cb:checked');
        const hasSelection = checked.length > 0;
        gerarBtn.disabled = !hasSelection;
        buscarHistoricoBtn.disabled = !hasSelection;
    }

    gerarBtn.addEventListener('click', () => {
        const checked = Array.from(document.querySelectorAll('.record-cb:checked')).map(cb => cb.value);
        if (checked.length === 0) return;

        // Reset UI
        gerarBtn.disabled = true;
        buscarHistoricoBtn.disabled = true;
        processingMsg.style.display = 'block';
        resultArea.style.display = 'none';
        errorGlobal.style.display = 'none';
        cartoesTematicos.innerHTML = '';

        fetch('/api/summaries', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                case_id: currentCaseId,
                entry_id: currentEntryId,
                record_ids: checked
            })
        })
        .then(async res => {
            if (!res.ok) {
                const err = await res.json();
                throw new Error(err.detail || 'Erro na requisição');
            }
            return res.json();
        })
        .then(data => {
            currentSummaryId = data.id;
            fontesOriginais = data.fontes_consultaveis;
            renderResult(data);
            processingMsg.style.display = 'none';
            resultArea.style.display = 'block';
            gerarBtn.disabled = false;
            buscarHistoricoBtn.disabled = false;
        })
        .catch(err => {
            errorGlobal.textContent = err.message;
            errorGlobal.style.display = 'block';
            processingMsg.style.display = 'none';
            gerarBtn.disabled = false;
            buscarHistoricoBtn.disabled = false;
        });
    });

    buscarHistoricoBtn.addEventListener('click', () => {
        const checked = Array.from(document.querySelectorAll('.record-cb:checked')).map(cb => cb.value);
        if (checked.length === 0) return;

        fetch('/api/summaries/search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                case_id: currentCaseId,
                entry_id: currentEntryId,
                record_ids: checked
            })
        })
        .then(res => res.json())
        .then(data => {
            historicoRevisoesConteudo.innerHTML = '';
            if (!data.history || data.history.length === 0) {
                historicoRevisoesConteudo.innerHTML = '<p>Nenhum resumo gerado ou revisado para esta exata combinação de registros.</p>';
            } else {
                data.history.forEach((exec, index) => {
                    const wrap = document.createElement('div');
                    wrap.style.marginBottom = '2rem';
                    wrap.style.borderBottom = '2px solid #ccc';
                    wrap.style.paddingBottom = '1rem';
                    
                    const dataExec = new Date(exec.created_at).toLocaleString('pt-BR');
                    wrap.innerHTML = `<h3>Geração ${data.history.length - index} (Criada em: ${dataExec})</h3>`;
                    
                    if (exec.reviews.length === 0) {
                        wrap.innerHTML += '<p style="color:#666;">Sem revisões, apenas a geração original do modelo está salva para este item.</p>';
                    }
                    
                    exec.reviews.forEach((rev, rIndex) => {
                        const div = document.createElement('div');
                        div.className = 'revisao-item';
                        const dataRev = new Date(rev.created_at).toLocaleString('pt-BR');
                        
                        let html = `<div class="revisao-meta">Revisão #${exec.reviews.length - rIndex} - Por: ${rev.reviewer} em ${dataRev}</div>`;
                        
                        ['consumo', 'familia', 'moradia'].forEach(tema => {
                            const bloco = rev.revised_json[tema];
                            if(bloco) {
                                html += `<div style="margin-bottom:0.5rem"><strong>${tema.toUpperCase()}:</strong><br>`;
                                html += `<span style="font-size:0.9rem; color:#444;">Situação: ${bloco.situacao_atual || '-'}</span><br>`;
                                html += `<span style="font-size:0.9rem; color:#444;">Mudanças: ${bloco.mudancas || '-'}</span></div>`;
                            }
                        });
                        
                        div.innerHTML = html;
                        wrap.appendChild(div);
                    });
                    
                    historicoRevisoesConteudo.appendChild(wrap);
                });
            }
            historicoModal.style.display = 'flex';
        })
        .catch(err => console.error('Erro na busca de histórico:', err));
    });

    function renderResult(data) {
        const temas = ['consumo', 'familia', 'moradia'];
        cartoesTematicos.innerHTML = '';

        // Exibir erros globais ou de validação
        if (data.erros && data.erros.length > 0) {
            const errDiv = document.createElement('div');
            errDiv.className = 'error-msg';
            errDiv.innerHTML = 'Problemas detectados:<br>' + data.erros.join('<br>');
            cartoesTematicos.appendChild(errDiv);
        }

        temas.forEach(tema => {
            const bloco = data.resumo[tema];
            if (!bloco) return;

            const card = document.createElement('div');
            card.className = 'tema-card';
            
            let html = `<h3>${tema}</h3>`;
            
            if (bloco.status_dados === 'sem_dados') {
                html += `<div class="campo">Não há informação sobre este tema nos registros selecionados.</div>`;
            } else {
                html += `
                    <div class="campo">
                        <strong>Situação atual:</strong>
                        <textarea class="edit-situacao" data-tema="${tema}">${bloco.situacao_atual || ''}</textarea>
                    </div>
                    <div class="campo">
                        <strong>Mudanças:</strong>
                        <textarea class="edit-mudancas" data-tema="${tema}">${bloco.mudancas || ''}</textarea>
                    </div>
                    <div class="campo">
                        <strong>Lacunas/Divergências:</strong>
                        <textarea class="edit-lacunas" data-tema="${tema}">${(bloco.lacunas_divergencias || []).join('\n')}</textarea>
                    </div>
                    <div class="campo">
                        <strong>Fontes:</strong>
                        ${(bloco.evidencias || []).map(id => `<span class="fonte-link" data-id="${id}">${id}</span>`).join('')}
                    </div>
                `;
            }
            card.innerHTML = html;
            cartoesTematicos.appendChild(card);
        });

        document.getElementById('tempo-info').textContent = 
            `Tempo carga: ${data.tempos.load_seconds}s | Tempo geração: ${data.tempos.generation_seconds}s | Tempo total: ${data.tempos.total_seconds}s`;

        document.querySelectorAll('.fonte-link').forEach(link => {
            link.addEventListener('click', (e) => {
                const id = e.target.getAttribute('data-id');
                abrirFonte(id);
            });
        });
    }

    function abrirFonte(id) {
        const fonte = fontesOriginais[id];
        if (!fonte) return;
        document.getElementById('modal-titulo').textContent = `Registro: ${id}`;
        document.getElementById('modal-data').textContent = `Data: ${fonte.data}`;
        document.getElementById('modal-texto').textContent = fonte.texto_original;
        modal.style.display = 'flex';
    }

    closeBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });
    closeHistoricoBtn.addEventListener('click', () => {
        historicoModal.style.display = 'none';
    });
    
    window.addEventListener('click', (e) => {
        if (e.target === modal) modal.style.display = 'none';
        if (e.target === historicoModal) historicoModal.style.display = 'none';
    });

    salvarRevisaoBtn.addEventListener('click', () => {
        const revisor = document.getElementById('revisor-nome').value || 'Não identificado';
        const msg = document.getElementById('revisao-msg');
        
        const revised_json = {
            consumo: extrairTema('consumo'),
            familia: extrairTema('familia'),
            moradia: extrairTema('moradia')
        };

        fetch(`/api/summaries/${currentSummaryId}/reviews`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ reviewer: revisor, revised_json: revised_json })
        })
        .then(res => {
            if (res.ok) {
                msg.style.display = 'block';
                setTimeout(() => msg.style.display = 'none', 3000);
            }
        });
    });

    function extrairTema(tema) {
        const card = document.querySelector(`.edit-situacao[data-tema="${tema}"]`);
        if (!card) return { status_dados: 'sem_dados', situacao_atual: '', mudancas: '', lacunas_divergencias: [], evidencias: [] };
        
        return {
            status_dados: 'com_dados', // Simplificação para o protótipo revisado
            situacao_atual: document.querySelector(`.edit-situacao[data-tema="${tema}"]`).value,
            mudancas: document.querySelector(`.edit-mudancas[data-tema="${tema}"]`).value,
            lacunas_divergencias: document.querySelector(`.edit-lacunas[data-tema="${tema}"]`).value.split('\n').filter(l => l.trim()),
            evidencias: [] // Mantido vazio na revisão simplificada
        };
    }
});
