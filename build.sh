#!/bin/bash

# Create dist directory
mkdir -p dist

# Copy static files
cp -r static dist/
cp -r templates dist/

# Copy index.html if it exists, or create a basic one
if [ -f "templates/index.html" ]; then
    cp templates/index.html dist/
else
    echo "<!DOCTYPE html><html><head><title>MD Convert</title></head><body><h1>MD Convert</h1></body></html>" > dist/index.html
fi 