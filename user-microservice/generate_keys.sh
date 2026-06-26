#!/usr/bin/env bash
set -euo pipefail

KEYS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/keys"
mkdir -p "$KEYS_DIR"

if [ -f "$KEYS_DIR/private_key.pem" ] || [ -f "$KEYS_DIR/public_key.pem" ]; then
    echo "Ключи уже существуют в $KEYS_DIR"
    echo "Для перегенерации удалите их вручную."
    exit 0
fi

openssl genpkey -algorithm RSA -out "$KEYS_DIR/private_key.pem" -pkeyopt rsa_keygen_bits:2048
openssl rsa -pubout -in "$KEYS_DIR/private_key.pem" -out "$KEYS_DIR/public_key.pem"

echo "Ключи сгенерированы:"
echo "  $KEYS_DIR/private_key.pem"
echo "  $KEYS_DIR/public_key.pem"