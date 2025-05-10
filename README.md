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
