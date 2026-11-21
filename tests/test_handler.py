import json
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import handler  # noqa: E402


class SensorTempTests(unittest.TestCase):
    def test_publica_temp_con_atributos_para_filtros_sns(self):
        sns = MagicMock()
        sns.publish.return_value = {"MessageId": "mensaje-123"}
        with patch.object(handler.boto3, "client", return_value=sns), patch.object(
            handler.random, "randint", return_value=41
        ) as random_mock, patch.dict(
            os.environ,
            {"SENSOR_TOPIC_ARN": "arn:aws:sns:us-east-1:904208419583:TemaSensorIoT"},
        ):
            response = handler.lambda_handler({}, None)

        random_mock.assert_called_once_with(10, 60)
        self.assertEqual(response["statusCode"], 200)
        published = sns.publish.call_args.kwargs
        lectura = json.loads(published["Message"])
        self.assertEqual(lectura["tenant_id"], "FAB1")
        self.assertTrue(lectura["lectura_id"].startswith("TEMP."))
        self.assertEqual(lectura["lectura_datos"], {"medicion": 41, "unidad_medida": "CELSIUS"})
        self.assertEqual(published["MessageAttributes"]["sensor_id"]["StringValue"], "TEMP")
        self.assertEqual(published["MessageAttributes"]["medicion"], {"DataType": "Number", "StringValue": "41"})
        self.assertEqual(json.loads(response["body"])["sns_message_id"], "mensaje-123")


if __name__ == "__main__":
    unittest.main()
