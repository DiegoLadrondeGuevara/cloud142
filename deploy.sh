#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

region="${AWS_REGION:-${AWS_DEFAULT_REGION:-us-east-1}}"
stage='prod'
profile=''
email="${SENSOR_ALERT_EMAIL:-}"

while (($#)); do
  case "$1" in
    --email|--region|--stage|--profile)
      if (($# < 2)); then echo "Falta el valor de $1" >&2; exit 2; fi
      case "$1" in
        --email) email="$2" ;;
        --region) region="$2" ;;
        --stage) stage="$2" ;;
        --profile) profile="$2" ;;
      esac
      shift 2
      ;;
    *)
      echo "Opción desconocida: $1" >&2
      echo 'Uso: bash deploy.sh --email OTRO_CORREO [--stage prod] [--region us-east-1] [--profile PERFIL]' >&2
      exit 2
      ;;
  esac
done

if [[ ! "$email" =~ ^[^[:space:]@]+@[^[:space:]@]+\.[^[:space:]@]+$ ]]; then
  echo 'Indica --email con el otro correo que recibirá las alertas TEMP.' >&2
  exit 2
fi
command -v aws >/dev/null || { echo 'Falta AWS CLI.' >&2; exit 1; }
[[ -x ./node_modules/.bin/serverless ]] || { echo 'Ejecuta npm ci antes de desplegar.' >&2; exit 1; }

profile_args=()
if [[ -n "$profile" ]]; then profile_args=(--profile "$profile"); fi
aws_read() { aws --region "$region" "${profile_args[@]}" "$@"; }

account_id="$(aws_read sts get-caller-identity --query Account --output text)"
if [[ "$account_id" != '904208419583' ]]; then
  echo "Cuenta AWS inesperada: $account_id; se requiere 904208419583." >&2
  exit 1
fi

topic_arn="arn:aws:sns:$region:$account_id:TemaSensorIoT"
aws_read sns get-topic-attributes --topic-arn "$topic_arn" --query Attributes.TopicArn --output text >/dev/null
queue_url="$(aws_read sqs get-queue-url --queue-name ColaSensorIoTFAB1 --query QueueUrl --output text)"
aws_read dynamodb describe-table --table-name t_sensor_iot_FAB1 --query Table.TableName --output text >/dev/null

export SENSOR_TOPIC_ARN="$topic_arn"
export SENSOR_ALERT_EMAIL="$email"

echo "Cuenta: $account_id | Tema: $topic_arn | Cola: $queue_url | Stage: $stage"
echo "Suscripción de correo: $email (debe confirmarse desde el buzón)"
serverless_args=(deploy --stage "$stage" --region "$region")
if [[ -n "$profile" ]]; then serverless_args+=(--aws-profile "$profile"); fi
./node_modules/.bin/serverless "${serverless_args[@]}"

echo 'Despliegue terminado. Confirma la suscripción en el correo antes de esperar alertas.'
