import os
import shutil
import stat

def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)

count = 0
env_dirs = {'env', '.env', 'venv', '.venv'}

for root, dirs, files in os.walk('.', topdown=True):
    if any(env_dir in root.split(os.sep) for env_dir in env_dirs):
        continue
    
    for dir_name in dirs:
        if dir_name == '__pycache__':
            pycache_path = os.path.join(root, dir_name)
            try:
                shutil.rmtree(pycache_path, onerror=remove_readonly)
                count += 1
            except Exception as e:
                print(f'Erro ao deletar o diretório {pycache_path}: {e}')

print(f'{count} diretórios __pycache__ deletados com sucesso.')