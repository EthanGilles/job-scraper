#!/bin/sh
set -e
echo "Injecting runtime configuration..."

cat <<EOF > /usr/share/nginx/html/config.js
window.RUNTIME_CONFIG = {
  API_URL: "${API_URL:-http://localhost}",
  ENVIRONMENT: "${ENVIRONMENT:-development}"
};
EOF

echo "Runtime config written:"
cat /usr/share/nginx/html/config.js

exec "$@"
