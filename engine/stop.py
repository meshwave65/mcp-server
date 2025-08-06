# ~/home/sofia/engine/stop.py
# VERSÃO ATUALIZADA: Procura pelo novo nome 'sentinel.py'.

import psutil
import os
import signal
import time

print("--- 🛑 Iniciando o Encerramento de TODOS os Serviços do Ecossistema SOFIA 🛑 ---")

def find_and_kill(target_name, target_string_in_cmd):
    """Encontra e mata processos que correspondem a uma string de comando."""
    pids_found = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = ' '.join(proc.info['cmdline'])
            # --- CORREÇÃO CRÍTICA ---
            # Procura pelo novo nome 'sentinel.py'
            if target_string_in_cmd in cmdline and proc.pid != os.getpid():
                pids_found.append(proc.info['pid'])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    
    if not pids_found:
        return False

    print(f"  -> Encontrados PIDs para '{target_name}': {pids_found}")
    for pid in pids_found:
        try:
            os.kill(pid, signal.SIGTERM)
            print(f"  ✅ Sinal de encerramento enviado para o PID {pid}.")
        except Exception as e:
            print(f"  ❌ Falha ao encerrar o PID {pid}: {e}")
    return True

# --- PASSADA 1: MATAR O SENTINELA PRIMEIRO ---
print("\n[PASSO 1/2] Procurando e encerrando o processo do Sentinela...")
# --- CORREÇÃO CRÍTICA ---
# A string de busca agora é 'sentinel.py'
sentinel_killed = find_and_kill("Sentinela", "sentinel.py")
if sentinel_killed:
    print("Aguardando 2 segundos para garantir o encerramento do Sentinela...")
    time.sleep(2)
else:
    print("Nenhum processo do Sentinela encontrado.")

# --- PASSADA 2: LIMPAR OS PROCESSOS FILHOS RESTANTES ---
print("\n[PASSO 2/2] Procurando e encerrando os serviços restantes...")

services_to_kill = {
    "Uvicorn": "uvicorn",
    "Vite/NPM": "vite",
    "Ngrok": "ngrok http"
}

any_killed_in_pass2 = False
for name, cmd_str in services_to_kill.items( ):
    if find_and_kill(name, cmd_str):
        any_killed_in_pass2 = True

if not sentinel_killed and not any_killed_in_pass2:
    print("\nNenhum serviço ativo do Ecossistema SOFIA foi encontrado.")
else:
    print("\n✅ Processo de encerramento concluído.")

