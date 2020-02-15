# risk_api
Django RESTful API for managing restaurant health inspection history

## Engineering Narrative:
https://docs.google.com/document/d/1ANhoOqOXt211WCpppfI44l1tBQbv-3UnaW4VlJ7XnfE/edit?usp=sharing

### Prompt:

Create an API, written in Python 3, which can accomplish the following tasks using separate endpoints:

Receive a JSON payload representing a public health inspection at a restaurant. The payload should be validated, then stored if valid. Whether the payload is valid or invalid, an appropriate response should be returned.
Given an inspection ID, return the associated record.
Given a restaurant ID, return a summary of its inspection history based on all stored inspections. The summary should contain dates and IDs of the restaurant's inspections, the average inspection score, and the average number of violations per inspection.


