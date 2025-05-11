from opcua import ua, Server
import pandas as pd
import itertools
import time

CSV_PATH = r"data.csv"            # ваш архив
ENDPOINT = "opc.tcp://0.0.0.0:4840"  # адрес OPC UA-сервера
PUBLISH_PERIOD = 1.0                 # период (сек.) между публикациями

# --- читаем данные -----------------------------------------------------------
df = (
    pd.read_csv(
        CSV_PATH,
        skiprows=[1],                 # пропустить 2-ю строку-заглушку
        parse_dates=["DATETIME"]      # сразу преобразуем в datetime
    )
)

# --- готовим OPC UA-сервер ---------------------------------------------------
srv = Server()
srv.set_endpoint(ENDPOINT)

uri = "https://data-science.uz/telemetry"
idx = srv.register_namespace(uri)

root = srv.get_objects_node()
well_obj = root.add_object(idx, "Well")      # <Objects>/<Well>/…

# создаём переменные по именам столбцов, кроме времени
nodes = {
    col: well_obj.add_variable(idx, col, ua.Variant(0.0, ua.VariantType.Double))
    for col in df.columns if col != "DATETIME"
}
for node in nodes.values():
    node.set_writable()                      # разрешаем внешнюю запись, если нужно

time_node = well_obj.add_variable(idx, "DATETIME", df["DATETIME"].iloc[0])
time_node.set_writable()

# --- бесконечная публикация --------------------------------------------------
def main():
    srv.start()
    print("OPC UA server started:", ENDPOINT)

    try:
        # itertools.cycle делает бесконечный итератор поверх DataFrame
        for row in itertools.cycle(df.itertuples(index=False)):
            # обновляем время и все числовые теги
            time_node.set_value(row.DATETIME)
            for col, node in nodes.items():
                node.set_value(getattr(row, col))

            time.sleep(PUBLISH_PERIOD)
    finally:
        srv.stop()
        print("Server stopped")

if __name__ == "__main__":
    main()


