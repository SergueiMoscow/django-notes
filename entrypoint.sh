#!/bin/sh
poetry run gunicorn django_notes.asgi:application -k uvicorn.workers.UvicornWorker -b :8082
