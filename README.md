# FastAPI PG starting template

As the name suggests, this is a starting template. A very minimal implementation of FastAPI with PostgreSql.

## To install dependencies

`pip install -r requirements.txt`

## To run the application locally

`uvicorn app.main:app --reload`

## Important notes

- This is a starting template
- Very minimal implementation of authentication with JWT token, and slight intro to roles
- Very minimal Dockerfile and docker-compose files
- Built everything on [Python 3.10](https://www.python.org/downloads/release/python-3100/). However, [Python 3.11](https://www.python.org/downloads/release/python-3110/) will support everything as well. 

## Mentions

This whole starting template wouldn't be possible without the exceptional documentation and easy approach that [FastAPI](https://fastapi.tiangolo.com/) has

If you're looking to dive deeper and build on top of this template, make sure to read their documentation as it offers great examples

None of this code is entirely mine, I based everything on [this video](https://www.youtube.com/watch?v=0sOvCWFmrtA&t=26670s) and added a few tweaks of my own based on [FastAPI](https://fastapi.tiangolo.com/) documentation

**Feel free to clone or commit any improvements, the purpose of this repo is to streamline project generation** 
