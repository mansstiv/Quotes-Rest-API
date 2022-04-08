# Quotes-Rest-API

<b>Implemented a REST API that manages quotes.</b>

## Tech Stack

<p>
   <a src="#"><img src="https://img.icons8.com/color/48/000000/python.png"/></a>
<a src="#"><img src="https://img.icons8.com/color/48/000000/flask.png"/></a>
<a src="#"><img src="https://img.icons8.com/color/48/000000/mongodb.png"/></a>
<a src="#"><img src="https://img.icons8.com/color/48/000000/docker.png"/></a>
</p>

## Part 1: Implementation

A <b>quote</b> has the following fields:

* **author** (string): The name of the author of the quote (optional).
    * e.g. 'Oscar Wilde'
* **text** (string): The text of the quote (mandatory). 
    * e.g. 'The truth is rarely pure and never simple.'

The API supports the following operations.

* Create a quote: 
    * ```/quotes, method=POST```
    * Fields of quote should be provided in body of request in a json format.
* Update a quote with a specific ID:
    * ```/quotes/<id>, method=PUT``` 
    * Fields of quote should be provided in body of request in a json format.
* Get a quote with a specific ID: 
    * ```/quotes/<id>, method=GET```
* Delete a quote with a specific ID:
    * ```/quotes/<id>, method=DELETE```
* Get a random quote:
    * ```/quotes/random, method=GET```
* Get all quotes:
    * ```/quotes, method=GET```
* Get quotes that contain specific text (e.g. "discover"):
    * ```/quotes/substring, method=GET```
    * Substring of quote should be provided as a value in body of request in a json format. Name of key can be anything you want. 

<i>(id in endpoint is the object id generated automatically in the field '_id')</i>

## Part 2: Testing

Tested with <b>pytest</b> endpoints that create, update and return a quote. 

## Part 3: Containerization

Wrote <b>Dockerfile</b> for the application. <br><br>
Wrote a <b>Compose file</b> to define and run the application as a set of containers (one container for the application, one container for the database). <br><br>
Used <b>Docker</b> and <b>Docker Compose</b>.

## Part 4: Running
```
# create and start (the first run takes time to build the image)
docker-compose up

# stop/restart
docker-compose stop
docker-compose start

# stop and remove
docker-compose down -v

# run tests
docker-compose run app python app_test.py
```
