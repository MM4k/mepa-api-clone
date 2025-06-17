#!/bin/bash
set -e errexit
set -e pipefail
set -e nounsetcle
set -e xtrace

C='\e[0;36m'     # cyan
Y='\033[0;33m'   # yellow
G='\033[0;32m'   # green 
B='\033[0;34m'   # blue
W='\033[0;37m'   # white
E='\033[0m'      # end

SITE_NAME="Monitoramento de Energia em Plataforma Aberta"

echo "${C}_________________________________________________________________________________________________________${E}"
echo "${C}=> CHECK INTEGRITY (check)                                                                               ${E}"
python manage.py check

echo "${C}_________________________________________________________________________________________________________${E}"
echo "${C}=> STARTING CRON                                                                                         ${E}"
echo 'Cronjobs mec-cron in operating system'
/bin/cp /app/mepa-api/cronjob/cronjob /etc/cron.d/mec-cron
crontab /etc/cron.d/mec-cron
cron

echo "${C}_________________________________________________________________________________________________________${E}"
echo "${C}=> MAKING MIGRATIONS (makemigrations)                                                                    ${E}" 
python manage.py makemigrations

echo "${C}_________________________________________________________________________________________________________${E}"
echo "${C}=> APPLYING MIGRATIONS (migrate)                                                                         ${E}"
python manage.py migrate

echo "${C}_________________________________________________________________________________________________________${E}"
echo '\e[33;36m=> RUNNING SERVER (runserver) \e[0;33m                                                                  '
echo " ${Y}                                                    __    ${E}${B}  ______  _____________________ _______   "
echo " ${Y}                                                  /    \  ${E}${B}  ___   |/  /___  ____/___  __ \___    |  "
echo " ${Y}                                                 /__    \ ${E}${B}  __  /|_/ / __/ __/   __  /_/ /__  /| |  "
echo " ${Y}                                                 \  /\  / ${E}${B}  _/ /  / /  _/ /___   _/ ____/ _/ ___ |  "
echo " ${Y}                                                  \/__\/  ${E}${B}  /_/  /_/   /_____/   /_/      /_/  |_|  "
echo "Starting ${W}"${API_SERVICE_NAME}"${E} - ${G}"${API_URL}"${E}             ${W}"${SITE_NAME}"${E}                 "
echo "${C}_________________________________________________________________________________________________________${E}"
python manage.py runserver ${API_HOST}:${API_PORT} 
