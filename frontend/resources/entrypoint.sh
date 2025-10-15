#!/bin/sh
set -e
echo "Injecting runtime configuration..."

cat <<EOF > /usr/share/nginx/html/config.js
window.RUNTIME_CONFIG = {
  API_URL: "${API_URL:-https://default-api.local}",
  ENVIRONMENT: "${ENVIRONMENT:-development}"
};
EOF

echo "Runtime config written:"
cat /usr/share/nginx/html/config.js

exec "$@"
