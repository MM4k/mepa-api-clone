#!/bin/bash

echo "Iniciando seeding para teste de usabilidade..."
export NUM_UNIVERSITIES=$1
cat scripts/seed_ut.py | ./manage.py shell