# backup/backup_db.py
import os
import shutil
import datetime
import sys

def backup_database():
    """
    Cria um backup timestamped (com data e hora) do arquivo 
    de banco de dados SQLite.
    """
    
    # --- Definição dos Caminhos ---
    
    # 1. Encontra o caminho absoluto deste script (backup/backup_db.py)
    script_path = os.path.abspath(__file__)
    
    # 2. Encontra o diretório onde o script está (a pasta 'backup')
    backup_dir = os.path.dirname(script_path)
    
    # 3. Encontra a raiz do projeto (a pasta 'eizyauto', pai da pasta 'backup')
    project_root = os.path.dirname(backup_dir)
    
    # 4. Define o nome e o caminho do banco de dados original (na raiz)
    database_name = "eizy_auto.db"
    source_db_path = os.path.join(project_root, database_name)
    
    # --- Verificações ---
    
    # Verifica se o banco de dados original existe
    if not os.path.exists(source_db_path):
        print(f"Erro: Banco de dados de origem não encontrado em '{source_db_path}'")
        print("Verifique se o nome do banco ('eizy_auto.db') está correto e na raiz do projeto.")
        return

    # O diretório de backup já existe (é onde este script está),
    # então não precisamos criá-lo.

    # --- Criar nome do arquivo de backup ---
    
    # Formato: eizy_auto.db_backup_ANO-MES-DIA_HORA-MINUTO-SEGUNDO.db
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_file_name = f"{database_name}_backup_{timestamp}.db"
    
    # 5. Define o caminho completo de destino para o backup
    dest_db_path = os.path.join(backup_dir, backup_file_name)

    # --- Executar o Backup ---
    try:
        # Copia o arquivo (shutil.copy2 preserva metadados como data de modificação)
        shutil.copy2(source_db_path, dest_db_path)
        
        print("\n--- Backup do Banco de Dados Concluído com Sucesso ---")
        print(f"Origem: {source_db_path}")
        print(f"Destino: {dest_db_path}")
        print("-------------------------------------------------------")

    except Exception as e:
        print(f"\nOcorreu um erro ao tentar copiar o banco de dados: {e}")

# --- Ponto de Entrada ---
# Isso permite que o script seja executado diretamente do terminal
# com: python backup/backup_db.py
if __name__ == "__main__":
    
    # Adiciona a raiz do projeto ao sys.path para garantir importações
    # (embora este script não use, é uma boa prática)
    project_root_for_imports = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if project_root_for_imports not in sys.path:
        sys.path.insert(0, project_root_for_imports)

    backup_database()
