#!/bin/bash


echo "Starting containers. Please, wait..."
docker compose -f=docker-compose-test.yml up --build --abort-on-container-exit --quiet-pull

compose_up_return_code=$?
if [ $compose_up_return_code -eq 0 ]
then
  echo "All tests were passed successfully."
elif [ $compose_up_return_code -eq 1 ];
then
  echo "Containers encountered an error or were manually stopped."
else
  echo "WHAT ARE THESE ERRORS"
fi


docker compose -f=docker-compose-test.yml down

exit 0
