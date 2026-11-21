# Capturas para entregar

Guarda capturas reales del laboratorio con estos nombres:

1. `01-serverless.png`: `serverless.yml` con v3, org, `LabRole`, regla programada y filtro TEMP `>40`.
2. `02-despliegue.png`: salida de `bash deploy.sh --email ...` con el stack desplegado. Oculta credenciales o tokens si aparecieran.
3. `03-confirmacion-sns.png`: correo de confirmación de SNS y estado confirmado de la suscripción. Evita mostrar datos personales innecesarios.
4. `04-lectura-temp.png`: salida de la invocación o log con `sensor_id` implícito en `lectura_id=TEMP...`, medición entre 10 y 60 y unidad `CELSIUS`.
5. `05-dynamodb.png`: consulta de `t_sensor_iot_FAB1` con al menos una lectura `TEMP` insertada.
6. `06-alerta-correo.png`: correo de alerta con una lectura TEMP mayor que 40 CELSIUS.

El filtro de correo se aplica a los atributos SNS `tenant_id`, `sensor_id` y `medicion`. La suscripción debe confirmarse en el buzón antes de esperar el correo de alerta.
