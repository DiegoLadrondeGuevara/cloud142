import json
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import consumer  # noqa: E402


class ConsumerTests(unittest.TestCase):
    def test_procesa_todo_el_lote_sns_sqs(self):
        lecturas = [
            {"tenant_id": "FAB1", "lectura_id": "CO2.1", "lectura_datos": {"medicion": 700, "unidad_medida": "PPM"}},
            {"tenant_id": "FAB1", "lectura_id": "TEMP.2", "lectura_datos": {"medicion": 50, "unidad_medida": "CELSIUS"}},
        ]
        event = {
            "Records": [
                {"body": json.dumps({"Message": json.dumps(lectura)})}
                for lectura in lecturas
            ]
        }
        table = MagicMock()
        boto3_mock = MagicMock()
        boto3_mock.resource.return_value.Table.return_value = table

        with patch.object(consumer, "boto3", boto3_mock), patch.dict(
            os.environ, {"SENSOR_TABLE_NAME": "t_sensor_iot_FAB1"}
        ):
            response = consumer.lambda_handler(event, None)

        self.assertEqual(response["lecturas_insertadas"], 2)
        self.assertEqual(table.put_item.call_count, 2)
        self.assertEqual(
            [call.kwargs["Item"]["lectura_id"] for call in table.put_item.call_args_list],
            ["CO2.1", "TEMP.2"],
        )


if __name__ == "__main__":
    unittest.main()
