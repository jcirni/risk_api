# risk_api
Django RESTful API for managing restaurant health inspection history

## Set Up
run the following commands to get started:
```
source ./bin/setup.sh
./bin/start.sh [:optional port number]
```
risk_api will spin up the Django WSGI server and run on your local
environment at the specified port or 8000 by default

You can view the browsable api at root endpoint:
http://127.0.0.1:8000/api/
http://localhost:8000/api/

The app will run in debug mode allowing you to see all requests
processed in your terminal

API supports JSON requests at the following endpoints:

| Endpoint | Command | Description |
| --- | --- | --- |
| /api/inspection/ | LIST | Lists all inspections saved |
| /api/inspection/ | POST | \[JSON\] Creates a new record of an inspection |
| /api/inspection/<inspection_id\> | GET | retrieves specified inspection |
| /api/restaurant/ | LIST | Lists all restaurants saved |
| /api/restaurant/ | POST | \[JSON\]Creates new restaurant record |
| /api/restaurant/\<restaurant_id\> | GET | Retrieves specified restaurant and related history |


## Engineering Narrative:
https://docs.google.com/document/d/1ANhoOqOXt211WCpppfI44l1tBQbv-3UnaW4VlJ7XnfE/edit?usp=sharing

### Prompt:

Create an API, written in Python 3, which can accomplish the following tasks using separate endpoints:

Receive a JSON payload representing a public health inspection at a restaurant. The payload should be validated, then stored if valid. Whether the payload is valid or invalid, an appropriate response should be returned.
Given an inspection ID, return the associated record.
Given a restaurant ID, return a summary of its inspection history based on all stored inspections. The summary should contain dates and IDs of the restaurant's inspections, the average inspection score, and the average number of violations per inspection.


