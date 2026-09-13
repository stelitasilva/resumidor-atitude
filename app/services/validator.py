import re
from typing import List, Dict, Any
from app.models import Record

TEMAS = ("consumo", "familia", "moradia")

def validar_resumo(resumo: Dict[str, Any], registros: List[Record]) -> List[str]:
    erros = []
    fontes = {r.id: r for r in registros}
    
    if set(resumo.keys()) != set(TEMAS):
        erros.append("A saída não contém exatamente os três temas obrigatórios.")
        
    for tema in TEMAS:
        bloco = resumo.get(tema, {})
        if not isinstance(bloco, dict):
            erros.append(f"{tema}: formato inválido.")
            continue
            
        evidencias = bloco.get("evidencias", [])
        status_dados = bloco.get("status_dados")
        
        if status_dados == "sem_dados" and evidencias:
            erros.append(f"{tema}: tema sem dados não deve conter evidências.")
        if status_dados != "sem_dados" and not evidencias:
            erros.append(f"{tema}: tema com dados sem evidências.")
            
        for registro_id in evidencias:
            if registro_id not in fontes:
                erros.append(f"{tema}: fonte {registro_id} inexistente ou fora da seleção.")
                
        textos_fontes = " ".join(fontes[i].texto for i in evidencias if i in fontes)
        datas_fontes = {fontes[i].data for i in evidencias if i in fontes}
        # Adicionar formatos dd/mm/yyyy e dd/mm
        datas_fontes |= {f'{d[8:10]}/{d[5:7]}/{d[:4]}' for d in datas_fontes}
        datas_fontes |= {f'{d[8:10]}/{d[5:7]}' for d in datas_fontes if len(d) == 10}
        
        texto_saida = " ".join([
            bloco.get("situacao_atual", ""), 
            bloco.get("mudancas", ""),
            " ".join(bloco.get("lacunas_divergencias", [])),
        ])
        
        for data in re.findall(r'\b\d{2}/\d{2}(?:/\d{4})?\b', texto_saida):
            if data not in datas_fontes and data not in textos_fontes:
                erros.append(f"{tema}: data {data} não encontrada nas fontes citadas.")
                
    return erros
