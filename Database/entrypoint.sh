#!/bin/bash
while !</dev/tcp/db/5432; do sleep 1; done;

# python db_init.py initialize
# python app.py