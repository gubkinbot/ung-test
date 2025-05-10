# main.py
from datetime import datetime, timezone, timedelta
from fastapi import FastAPI, Query
from opc_client import OPCReader

app = FastAPI(title="OPC → JSON API")
reader = OPCReader()
reader.connect()        # цепляемся один раз при старте

POINT_CODE = "010620408500506"
DEVICE_SN = "А07FJ049"
DEVICE_TYPE = "AutoPilot"
METER_UNIT = 1

@app.get("/telemetry")
def get_telemetry(
    requestedDate: datetime = Query(datetime.now(timezone.utc), alias="requestedDate")
):
    snap = reader.read_snapshot()

    payload = {
        "requestedDate": requestedDate.replace(tzinfo=timezone.utc).isoformat(),
        "valuesCount": 1,
        "pointCode": POINT_CODE,
        "deviceSerialNumber": DEVICE_SN,
        "deviceType": DEVICE_TYPE,
        "meterUnitType": METER_UNIT,
        "values": [snap],            # кладём весь снимок «как есть»
    }
    return payload
