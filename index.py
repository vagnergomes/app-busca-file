#percorre diretorios em busca dos arquivo em tabela

import os
import shutil
import pandas as pd
from pathlib import Path

df = pd.read_excel("chaves.xlsx")

chaves_limpas = (
    df.iloc[:, 0]
    .dropna()
    .astype(str)
    .str.strip()
    .str.replace(r'^(NFe|NFE|nfe|CCe|CCE|cce)', '', regex=True) # Remove prefixos anteriores
    .tolist()
)

pasta_origem = Path(r"\\terrena10sap\B1_SHR\11-SKILL\PTS\MDFE\XML\MDFe\Produção\MDFe\Produção\20260804")
pasta_destino = Path(__file__).parent / "destino"
log_erros = Path(__file__).parent / "nao_encontrados.txt"

pasta_destino.mkdir(parents=True, exist_ok=True)

print("1/2 - Mapeando arquivos da rede (passo único)...")
todos_arquivos = []
for raiz, _, arquivos in os.walk(pasta_origem):
    for arq in arquivos:
        todos_arquivos.append((arq, os.path.join(raiz, arq)))

print(f"Mapeamento concluído. {len(todos_arquivos)} arquivos encontrados no servidor.\n")
print("2/2 - Buscando arquivos com prefixo 'CCe'...")

nao_encontrados = []
encontrados_count = 0

for i, chave_num in enumerate(chaves_limpas, 1):
    chave_busca = f"{chave_num}"
    encontrado = False
    
    for nome_arq, caminho_completo in todos_arquivos:
        if chave_busca in nome_arq:
            shutil.copy(caminho_completo, pasta_destino)
            print(f"[{i}/{len(chaves_limpas)}] ✔ Copiado: {nome_arq}")
            encontrado = True
            encontrados_count += 1
            
    if not encontrado:
        nao_encontrados.append(chave_busca)
        print(f"[{i}/{len(chaves_limpas)}] ✖ Não encontrado: {chave_busca}")

# Salva log de não encontrados
with open(log_erros, "w", encoding="utf-8") as f:
    for item in nao_encontrados:
        f.write(f"{item}\n")

print("\n--- FINALIZADO ---")
print(f"Arquivos Copiados: {encontrados_count}")
print(f"Não Encontrados: {len(nao_encontrados)} (salvos em nao_encontrados.txt)")