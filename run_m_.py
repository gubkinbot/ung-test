# run_services_mp.py
import multiprocessing as mp
import subprocess
import sys
import time

def start_opc():
    # Запустить OPC_UI.py «как есть»
    subprocess.run([sys.executable, "OPC_UI.py"])

def start_api():
    # uvicorn как отдельный процесс
    subprocess.run([sys.executable, "-m", "uvicorn",
                    "main:app", "--host", "127.0.0.1", "--port", "8001"])

if __name__ == "__main__":
    p_opc = mp.Process(target=start_opc)
    p_api = mp.Process(target=start_api)

    p_opc.start()
    time.sleep(2)      # дать OPC успеть подняться (при желании → health-check)
    p_api.start()

    # Ожидаем завершения обоих (Ctrl-C убьёт оба)
    p_opc.join()
    p_api.join()
