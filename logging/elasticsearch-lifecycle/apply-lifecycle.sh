
#!/bin/sh
set -eu

ES_URL="https://logs-es-http.logging.svc:9200"
CA_CERT="/certs/ca.crt"

echo "Applying Elasticsearch ILM policy..."

curl --fail-with-body --silent --show-error \
  --cacert "$CA_CERT" \
  -u "elastic:${ES_PASSWORD}" \
  -H "Content-Type: application/json" \
  -X PUT "${ES_URL}/_ilm/policy/kubernetes-logs-7d" \
  --data-binary @/config/ilm-policy.json

echo "Applying index template..."

curl --fail-with-body --silent --show-error \
  --cacert "$CA_CERT" \
  -u "elastic:${ES_PASSWORD}" \
  -H "Content-Type: application/json" \
  -X PUT "${ES_URL}/_index_template/kubernetes-logs-template" \
  --data-binary @/config/index-template.json

echo "Attaching policy to existing Kubernetes log indices..."

curl --fail-with-body --silent --show-error \
  --cacert "$CA_CERT" \
  -u "elastic:${ES_PASSWORD}" \
  -H "Content-Type: application/json" \
  -X PUT "${ES_URL}/kubernetes-v2-*/_settings" \
  -d '{"index.lifecycle.name":"kubernetes-logs-7d"}'

echo "ILM policy and index template applied successfully."
