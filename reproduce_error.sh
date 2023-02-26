#!/bin/bash

echo "Creating user lcrown"
FIRST='{"firstname": "Lucas", "lastname": "Crownover", "username": "lcrown", "email": "lcrown@example.org", "is_pi": "true"}'
sleep 1
curl -X POST -H "Content-Type: application/json" -d "$FIRST" http://localhost:8000/users/
printf "\n\n"

echo "Creating user jimmy, sponsored by lcrown"
SECOND='{"firstname": "Jimmy", "lastname": "Neutron", "username": "jimmy", "email": "jimmy@example.org", "is_pi": "false", "sponsor_id": 1}'
sleep 1
curl -X POST -H "Content-Type: application/json" -d "$SECOND" http://localhost:8000/users/
printf "\n\n"

echo "Creating pirg pirgOne, owned by lcrown"
THIRD='{"name": "pirgOne", "owner_id": 1, "user_ids": [2], "admin_ids": [1]}'
sleep 1
curl -X POST -H "Content-Type: application/json" -d "$THIRD" http://localhost:8000/pirgs/
printf "\n\n"

echo "Adding lcrown as user of pirgOne"
FOURTH='{"user_id": 1}'
sleep 1
curl -X POST -H "Content-Type: application/json" -d "$FOURTH" http://localhost:8000/pirgs/pirgOne/users
printf "\n\n"

echo "Removing jimmy from pirgOne"
sleep 1
curl -X DELETE -H "Content-Type: application/json" http://localhost:8000/pirgs/pirgOne/users/2
printf "\n\n"

echo "Adding test group with lcrown user to pirgOne"
FIFTH='{"name": "test", "pirg_id": 1, "user_ids": [1]}'
sleep 1
curl -X POST -H "Content-Type: application/json" -d "$FIFTH" http://localhost:8000/pirgs/pirgOne/groups
printf "\n\n"

echo "Adding jimmy to test group"
SIXTH='{"user_id": 2}'
sleep 1
curl -X POST -H "Content-Type: application/json" -d "$SIXTH" http://localhost:8000/pirgs/pirgOne/groups/1/users
printf "\n\n"

echo "Removing lcrown from test group"
sleep 1
curl -X DELETE -H "Content-Type: application/json" http://localhost:8000/pirgs/pirgOne/groups/1/users/1
printf "\n\n"

# echo "Deleting test group"
# sleep 1
# curl -X DELETE -H "Content-Type: application/json" http://localhost:8000/pirgs/pirgOne/groups/1
# printf "\n\n"
