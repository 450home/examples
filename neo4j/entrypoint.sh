#!/bin/bash

if [ -n "$NEO4J_AUTH_PASSWORD" ]; then
    neo4j-admin dbms set-initial-password "$NEO4J_AUTH_PASSWORD"
fi

exec neo4j console
