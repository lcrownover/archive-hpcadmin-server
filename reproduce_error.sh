#!/bin/bash

FIRST='{"firstname": "Lucas", "lastname": "Crownover", "username": "lcrown", "email": "lcrown@example.org", "is_pi": "true"}'
SECOND='{"firstname": "Jimmy", "lastname": "Neutron", "username": "jimmy", "email": "jimmy@example.org", "is_pi": "false", "sponsor_id": 1}'
THIRD='{"name": "pirgOne", "owner_id": 1, "user_ids": [2], "admin_ids": [1]}'
FOURTH='{"user_id": 1}'

echo "submitting data:"
echo $FIRST
sleep 1
echo "got data:"
curl -X POST -H "Content-Type: application/json" -d  "$FIRST" http://localhost:8000/users/

echo "submitting data:"
echo $SECOND
sleep 1
echo "got data:"
curl -X POST -H "Content-Type: application/json" -d  "$SECOND" http://localhost:8000/users/

echo "submitting data:"
echo $THIRD
sleep 1
echo "got data:"
curl -X POST -H "Content-Type: application/json" -d  "$THIRD" http://localhost:8000/pirgs/

echo "submitting data:"
echo $FOURTH
sleep 1
echo "got data:"
curl -X POST -H "Content-Type: application/json" -d  "$FOURTH" http://localhost:8000/pirgs/pirgOne/users

sleep 1
echo "got data:"
curl -X GET -H "Content-Type: application/json" http://localhost:8000/users/1
