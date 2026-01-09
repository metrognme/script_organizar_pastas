import shutil
from pathlib import Path
from datetime import datetime

pasta_origem = Path('/home/seu_usuario/Downloads') # --- MUDAR AQUI
pasta_destino = Path('/home/seu_usuario/Downloads/para_organizar') # --- MUDAR AQUI
arquivo_log = pasta_destino / "log_mudancas.txt"

pasta_destino.mkdir(exist_ok=True)

def gravar_log(mensagem):
    agora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    with open(arquivo_log, 'a', encoding='utf-8') as f:
        f.write(f"[{agora}] {mensagem}\n")

print("[*] Iniciando organização...")

for arquivo in pasta_origem.iterdir():
    if arquivo.is_dir() or arquivo.name == "auto_downloads.py" or arquivo.name == arquivo_log.name:
        continue
        
    if arquivo.suffix:
        extensao = arquivo.suffix[1:].lower()
    else:
        extensao = 'sem_extensao'

    subpasta = pasta_destino / extensao
    subpasta.mkdir(exist_ok=True, parents=True)
    destino_final = subpasta / arquivo.name

    try:
        if not destino_final.exists():
            shutil.move(arquivo, destino_final)
            print(f'[OK] "{arquivo.name}" movido para --> "{extensao}".')
            gravar_log(f"SUCESSO: '{arquivo.name}' movido para '{extensao}'")
        else:
            print(f"\n[!] CONFLITO ENCONTRADO: '{arquivo.name}'")
            print(f"    Já existe um arquivo com este nome na pasta '{extensao}'.")
            print("    [1] Renomear (Salva como '_copia_DATA')")
            print("    [2] Substituir (Apaga o antigo da pasta organizada)")
            print("    [3] Pular (Não faz nada)")
            
            opcao = input("      >>> Escolha uma opção (1-3): ").strip()

            if opcao == '1':
                timestamp = datetime.now().strftime("%d-%m-%Y_%H%M%S")
                novo_nome = f"{arquivo.stem}_copia_{timestamp}{arquivo.suffix}"
                novo_destino = subpasta / novo_nome

                shutil.move(arquivo, novo_destino)
                print(f"[@] Renomeado para: {novo_nome} e movido.")
                gravar_log(f"RENOMEADO: '{arquivo.name}' virou '{novo_nome}'")

            elif opcao == '2':
                shutil.move(arquivo, destino_final)
                print(f"    [v] Arquivo substituído.")
                gravar_log(f"SUBSTITUÍDO: '{arquivo.name}' na pasta '{extensao}'.")

            else:
                print(f"    [x] Arquivo ignorado.")
                gravar_log(f"PULADO: '{arquivo.name}' ignorado pelo usuário.")

    except Exception as e:
        msg_erro = f"ERRO CRÍTICO ao mover '{arquivo.name}': {e}"
        print(msg_erro)
        gravar_log(msg_erro)

print("\n" + "-"*30)
print("[*] Organização concluída! Verifique o log.")
