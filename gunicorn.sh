#!/bin/sh
gunicorn config.wsgi --timeout 300 -b 0.0.0.0:8000
