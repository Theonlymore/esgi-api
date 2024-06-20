#!/bin/bash
rm -rf esgi-api

git clone https://github.com/Theonlymore/esgi-api.git


docker-compose -f esgi-api/docker-compose.yml up --build -d
