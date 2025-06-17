#!/bin/bash
set -e errexit
set -e pipefail
set -e nounsetcle
set -e xtrace

B='\033[0;34m'   # blue
G='\033[0;32m'   # green 
E='\033[0m'      # end

echo "${B}_________________________________________________________________________________________________________${E}"
echo "${G}====> CHECK INTEGRITY (check) ${E}"
python manage.py check

echo "${B}_________________________________________________________________________________________________________${E}"
echo "${G}====> STARTING CRON ${E}"
echo 'Cronjobs mec-cron in operating system'
/bin/cp /app/mepa-api/cronjob/cronjob /etc/cron.d/mec-cron
crontab /etc/cron.d/mec-cron
cron

echo "${B}_________________________________________________________________________________________________________${E}"
echo "${G}====> APPLYING MIGRATIONS (migrate) ${E}"
python manage.py migrate --noinput 

echo "${B}_________________________________________________________________________________________________________${E}"
echo "${G}====> COLLECT STATIC FILES (collectstatic) ${E}"
python manage.py collectstatic --no-input

echo "${B}_________________________________________________________________________________________________________${E}"
echo "${G}====> RUNNING SERVER (gunicorn) ${E}"
num_cpus=$(grep -c ^processor /proc/cpuinfo)
num_workers=$((2 * num_cpus + 1))
gunicorn mec_energia.wsgi:application  --workers $num_workers --bind ${API_HOST}:${API_PORT}
