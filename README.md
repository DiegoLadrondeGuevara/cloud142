# Semana 14, sesión 2: ejercicio propuesto

El taller de clase ya tiene `TemaSensorIoT`, `ColaSensorIoTFAB1`, `t_sensor_iot_FAB1`, una Lambda que inserta las lecturas desde SQS y una Lambda que genera CO2. Este proyecto agrega el sensor `TEMP` para `FAB1` con lecturas aleatorias de **10 a 60 CELSIUS**. Publica las lecturas en el mismo tema SNS y añade una suscripción a **otro correo** para `tenant_id=FAB1`, `sensor_id=TEMP` y `medicion>40`.

Serverless Framework v3 administra una Lambda nueva, su regla programada cada minuto y la suscripción de correo. Así se conserva la Lambda de CO2 creada en clase. La cola y la Lambda consumidora existentes reciben también TEMP por el filtro `tenant_id=FAB1` y lo insertan en la misma tabla. El proyecto usa `org: diegoladrondeguevara`, la cuenta `904208419583` y únicamente `arn:aws:iam::904208419583:role/LabRole` como rol de ejecución; la plantilla no crea roles IAM.

## Despliegue en Bash o AWS CloudShell

Usa una dirección de correo distinta de la suscripción CO2 de clase. En la cuenta del laboratorio:

```bash
git clone https://github.com/DiegoLadrondeGuevara/cloud142.git
cd cloud142
npm ci
bash deploy.sh --email otro-correo@ejemplo.com
```

El script verifica la cuenta y consulta el tema, la cola y la tabla de la práctica. Si usas un perfil, añade `--profile nombre-del-perfil`; el stage predeterminado es `prod` y la región predeterminada es `us-east-1`. Los cambios de infraestructura se aplican con `serverless deploy`.

`LabRole` debe permitir `sns:Publish` sobre `TemaSensorIoT`. Las credenciales de despliegue deben permitir CloudFormation, Lambda, EventBridge, SNS, S3 y `iam:PassRole` para `LabRole`.

**Confirma la suscripción** desde el enlace que SNS enviará al otro correo. Sin esa confirmación no llegará ningún aviso. El filtro nuevo puede tardar hasta 15 minutos en aplicarse por completo; [AWS documenta esta propagación](https://docs.aws.amazon.com/sns/latest/dg/sns-subscription-filter-policies.html).

## Verificación

La regla de Serverless ejecuta TEMP cada minuto. También puedes invocar la Lambda para obtener una lectura de inmediato:

```bash
aws lambda invoke \
  --function-name semana14-sesion2-GenerarTEMP-prod \
  --region us-east-1 \
  --cli-binary-format raw-in-base64-out \
  --payload '{}' /tmp/lectura-temp.json
cat /tmp/lectura-temp.json
```

Para ver las lecturas TEMP guardadas por el consumidor de clase:

```bash
aws dynamodb scan \
  --table-name t_sensor_iot_FAB1 \
  --region us-east-1 \
  --filter-expression 'begins_with(lectura_id, :prefijo)' \
  --expression-attribute-values '{":prefijo":{"S":"TEMP."}}' \
  --query 'Items[].{lectura:lectura_id.S,medicion:lectura_datos.M.medicion.N,unidad:lectura_datos.M.unidad_medida.S}' \
  --output table
```

Las mediciones de 41 a 60 cumplen el filtro y deben llegar por correo después de confirmar la suscripción. Una lectura de 40 no cumple la condición `>40`. Para probar el código sin AWS:

```bash
python3 -m unittest discover -s tests -v
```

La guía de [capturas](evidencias/README.md) indica qué guardar para la entrega. Todavía no hay capturas de AWS: deben tomarse durante el despliegue en la cuenta del laboratorio y desde el correo confirmado.

## Referencias

- Enunciado: Taller 4 de la semana 14, diapositiva 15.
- [Serverless: ejecución programada](https://www.serverless.com/framework/docs/providers/aws/events/schedule).
- [CloudFormation: suscripción SNS](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-sns-subscription.html).
