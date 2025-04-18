#!/bin/bash

# Generate enclave signing key
openssl genrsa -3 -out enclave-key.pem 3072

# Generate attestation certificate
gramine-sgx-gen-private-key -k enclave-key.pem -o attestation-key.pem

# Generate remote attestation quote
gramine-sgx-get-quote -k attestation-key.pem -d /app -o quote.dat

# Verify quote with IAS
gramine-sgx-ias-verify -k attestation-key.pem -d /app -q quote.dat
