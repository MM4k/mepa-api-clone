#!/bin/bash

# Define cores para as mensagens
GREEN='\033[0;32m'
YELLOW='\033[1;34m'
PINK='\033[1;36m'
BLUE='\033[1;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "\e[1;36m----------------------------------------------------------------------------------------------------------\e[0m"
echo -e "\e[1;36m                                   DOCKER CLEANUP SCRIPT\e[0m"
echo -e "\e[1;36m----------------------------------------------------------------------------------------------------------\e[0m"
docker --version
docker compose version
echo ""

echo -e "${YELLOW}=> ALL CONTAINERS:${NC}"
docker container ls --all
echo "----------------------------------------------------------------------------------------------------------"
echo -e "${YELLOW}=> ALL IMAGES:${NC}"
docker images
echo "----------------------------------------------------------------------------------------------------------"
echo -e "${YELLOW}=> ALL VOLUMES:${NC}"
docker volume ls
echo "----------------------------------------------------------------------------------------------------------"

echo ""
echo -e "${RED}ATENÇÃO: Esta ação irá remover todos os containers, imagens, volumes e networks do Docker.${NC}"
echo -e "${RED}Dados podem ser perdidos.${NC}"
read -p "$(echo -e "${YELLOW}Deseja continuar? (s/n): ${NC}")" resposta

if [[ $resposta == "s" || $resposta == "S" ]]; then
    echo ''
    echo "----------------------------------------------------------------------------------------------------------"
    echo -e "${GREEN}=> STOPPING ALL CONTAINERS:${NC}"
    if [[ $(docker ps -aq) ]]; then docker stop $(docker ps -aq); fi
    echo "----------------------------------------------------------------------------------------------------------"
    echo -e "${GREEN}=> REMOVING ALL CONTAINERS${NC}"
    if [[ $(docker ps -aq) ]]; then docker rm -f $(docker ps -aq); fi
    echo "----------------------------------------------------------------------------------------------------------"
    echo -e "${GREEN}=> REMOVING ALL IMAGES${NC}"
    if [[ $(docker images -q) ]]; then docker rmi -f $(docker images -q); fi
    echo "----------------------------------------------------------------------------------------------------------"
    echo -e "${GREEN}=> REMOVING ALL VOLUMES${NC}"
    if [[ $(docker volume ls -q) ]]; then docker volume rm -f $(docker volume ls -q); fi
    echo "----------------------------------------------------------------------------------------------------------"
    echo -e "${GREEN}=> REMOVING ALL NETWORKS${NC}"
    if [[ $(docker network ls --filter type=custom -q) ]]; then docker network rm -f $(docker network ls --filter type=custom); fi
    echo "----------------------------------------------------------------------------------------------------------"
    echo -e "${GREEN}=> REMOVING ALL BUILDERS${NC}"
    docker builder prune -a -f
    echo "----------------------------------------------------------------------------------------------------------"


    echo ""
    echo -e "${GREEN}-------------------${NC}"
    echo -e "${GREEN}## AFTER CLEANER:${NC}"
    echo -e "${GREEN}-------------------${NC}"
    echo "----------------------------------------------------------------------------------------------------------"
    echo -e "${YELLOW}=> ALL CONTAINERS:${NC}"
    docker container ls --all
    echo "----------------------------------------------------------------------------------------------------------"
    echo -e "${YELLOW}=> ALL IMAGES:${NC}"
    docker images
    echo "----------------------------------------------------------------------------------------------------------"
    echo -e "${YELLOW}=> ALL VOLUMES:${NC}"
    docker volume ls
    echo "----------------------------------------------------------------------------------------------------------"
else
  echo -e "${RED}Action canceled.${NC}"
fi
