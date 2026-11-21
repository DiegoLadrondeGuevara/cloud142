"""Inserta todas las lecturas recibidas en un lote SQS desde SNS."""

import json
import os

import boto3


def lambda_handler(event, context):
    table = boto3.resource("dynamodb").Table(os.environ["SENSOR_TABLE_NAME"])
    processed = 0

    for record in event["Records"]:
        body = json.loads(record["body"])
        lectura = json.loads(body["Message"]) if "Message" in body else body
        if not isinstance(lectura, dict) or not {"tenant_id", "lectura_id", "lectura_datos"} <= lectura.keys():
            raise ValueError("Mensaje sin los campos de una lectura de sensor")
        table.put_item(Item=lectura)
        processed += 1
        print(json.dumps({"lectura_id": lectura["lectura_id"], "tenant_id": lectura["tenant_id"]}))

    return {"lecturas_insertadas": processed}
