"""Genera lecturas TEMP para FAB1 y las publica en el SNS de la práctica."""

import json
import os
import random
from datetime import datetime, timezone

import boto3


def lambda_handler(event, context):
    tenant_id = "FAB1"
    sensor_id = "TEMP"
    medicion = random.randint(10, 60)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d.%H:%M:%S.%f")
    lectura = {
        "tenant_id": tenant_id,
        "lectura_id": f"{sensor_id}.{timestamp}",
        "lectura_datos": {
            "medicion": medicion,
            "unidad_medida": "CELSIUS",
        },
    }

    respuesta_sns = boto3.client("sns").publish(
        TopicArn=os.environ["SENSOR_TOPIC_ARN"],
        Subject="Nueva Lectura Sensor TEMP",
        Message=json.dumps(lectura),
        MessageAttributes={
            "tenant_id": {"DataType": "String", "StringValue": tenant_id},
            "sensor_id": {"DataType": "String", "StringValue": sensor_id},
            "medicion": {"DataType": "Number", "StringValue": str(medicion)},
        },
    )
    print(json.dumps(lectura))
    return {
        "statusCode": 200,
        "body": json.dumps(
            {"lectura": lectura, "sns_message_id": respuesta_sns["MessageId"]}
        ),
    }
