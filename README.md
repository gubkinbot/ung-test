# ung-test

JUST RUN run_services.py file

Запуск на хосте
Копируем файлы на хост
  /var/www/www-root/python-opc-api
    /OPC_UI.py
    /data.csv
    /main.py
    /opc_client.py
    /requirements.txt
    /run_services.py

Добавляем в настройки Nginx
<br>
<code>
<b>location /api/ {
        proxy_pass         http://127.0.0.1:8001/;    # <-- обратите внимание на завершающий «/»
        proxy_set_header   Host            $host;
        proxy_set_header   X-Real-IP       $remote_addr;
        proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto $scheme;
    }
 </b> 
 </code>

 Запускаем Shell-клиент и выолняем сл. команды
  <code>
  apt install python3 python3-ven  
  source venv/bin/activate  
  pip install -r requirements.txt 

  Запуск файла (но сессия обрывается нужно перенести в службы сервера)
  python run_services.py     
  </code>

Запуск как службу
  Создаём файл /etc/systemd/system/opc_api.service 
<code>
      [Unit]
    Description=OPC UA server + FastAPI JSON gateway
    After=network.target
    
    [Service]
    User=root
    Group=root
    WorkingDirectory=/var/www/www-root/python-opc-api
    Environment="PATH=/var/www/www-root/python-opc-api/venv/bin"
    ExecStart=/var/www/www-root/python-opc-api/venv/bin/python3 run_services.py
    Restart=on-failure
    
    [Install]
    WantedBy=multi-user.target
</code>


  в терминале выполням команду
  <code>
  sudo systemctl daemon-reload
  sudo systemctl start opc_api 
  sudo systemctl status opc_api -n 20   
</code>

  Должно выйти 
  <code>
   opc_api.service - OPC UA server + FastAPI JSON gateway
     Loaded: loaded (;;file://data-science.uz/etc/systemd/system/opc_api.service/etc/systemd/system/opc_api.service;;; enabled; pre
set: enabled)
     Active: active (running) since Sun 2025-05-11 00:52:59 +05; 2s ago
   Main PID: 300351 (python3)                                                                                                      
      Tasks: 6 (limit: 2298)                                                                                                       
     Memory: 133.6M (peak: 133.8M)                                                                                                 
        CPU: 1.812s                                                                                                                
     CGroup: /system.slice/opc_api.service                                                                                         
             ├─300351 /var/www/www-root/python-opc-api/venv/bin/python3 run_services.py
             ├─300352 /var/www/www-root/python-opc-api/venv/bin/python3 run_services.py
             ├─300353 /var/www/www-root/python-opc-api/venv/bin/python3 OPC_UI.py
             ├─300355 /var/www/www-root/python-opc-api/venv/bin/python3 run_services.py
             └─300356 /var/www/www-root/python-opc-api/venv/bin/python3 -m uvicorn main:app --host 127.0.0.1 --port 8001
</code>
