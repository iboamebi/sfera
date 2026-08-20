#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")/.."

echo "==> Building production frontend"
npm run build

if [[ ! -d dist ]]; then
  echo "ERROR: dist/ was not created" >&2
  exit 1
fi

if [[ ! -f dist/index.html ]]; then
  echo "ERROR: dist/index.html is missing" >&2
  exit 1
fi

echo "==> Deploying dist/ to /var/www/sfera"
sudo -v
sudo rsync -a --delete dist/ /var/www/sfera/

echo "==> Fixing ownership"
sudo chown -R root:root /var/www/sfera

echo "==> Fixing directory permissions"
sudo find /var/www/sfera -type d -exec chmod 755 {} +

echo "==> Fixing file permissions"
sudo find /var/www/sfera -type f -exec chmod 644 {} +

echo "==> Production frontend deployed successfully"
