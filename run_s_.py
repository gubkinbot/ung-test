# run_services.py  (запускаем этот файл)
from threading import Thread
import uvicorn
from OPC_UI import run_opc_server          # функция из п.1
from main import app                       # FastAPI-приложение

if __name__ == "__main__":
    # OPC UA-сервер в фоновой нити (daemon, чтобы гасился вместе с основным процессом)
    t = Thread(target=run_opc_server, daemon=True)
    t.start()

    # HTTP-API (блокирует главный поток)
    uvicorn.run(app, host="0.0.0.0", port=8000, workers=1)
