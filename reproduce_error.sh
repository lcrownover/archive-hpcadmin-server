#!/bin/bash

curl -X POST -H "Content-Type: application/json" -d '{"firstname": "Lucas", "lastname": "Crownover", "username": "lcrown", "email": "lcrown@example.org", "is_pi": "true"}' http://localhost:8000/users/
curl -X POST -H "Content-Type: application/json" -d '{"firstname": "Jimmy", "lastname": "Neutron", "username": "jimmy", "email": "jimmy@example.org", "is_pi": "false", "sponsor_id": 1}' http://localhost:8000/users/
