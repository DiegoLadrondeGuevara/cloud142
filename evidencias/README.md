# Capturas para entregar

Guarda capturas reales del laboratorio con estos nombres:

1. `01-serverless.png`: `serverless.yml` actualizado con v3, org, `LabRole`, regla programada, filtro TEMP `>40` y consumidor SQS.
2. `02-despliegue.png`: salida del despliegue actualizado con ambas funciones (`generarSensorTemp` e `insertarLecturaSensor`). Oculta credenciales o tokens si aparecieran.
3. `03-confirmacion-sns.png`: correo de confirmación de SNS y estado confirmado de la suscripción. Evita mostrar datos personales innecesarios.
4. `04-lectura-temp.png`: salida de la invocación o log con `sensor_id` implícito en `lectura_id=TEMP...`, medición entre 10 y 60 y unidad `CELSIUS`.
5. `05-dynamodb.png`: consulta de `t_sensor_iot_FAB1` con al menos una lectura `TEMP` insertada. Reemplaza cualquier captura anterior de la tabla vacía.
6. `06-alerta-correo.png`: correo de alerta con una lectura TEMP mayor que 40 CELSIUS.
7. `07-trigger-sqs.png`: consulta que muestre el desencadenador de la nueva Lambda en estado `Enabled`.

El filtro de correo se aplica a los atributos SNS `tenant_id`, `sensor_id` y `medicion`. La suscripción debe confirmarse en el buzón antes de esperar el correo de alerta.
