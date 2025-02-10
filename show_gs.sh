#!/bin/bash

# Check if a parameter is passed
if [ -z "$1" ]; then
  echo "Usage: $0 <directory>"
  exit 1
fi

# Assign the parameter to a variable
DIRECTORY=$1

# List the contents of the specified directory
echo "Listing contents of gs://forgood-temp-storage/rag_bench/swe/$DIRECTORY:"
gsutil ls gs://forgood-temp-storage/rag_bench/swe/$DIRECTORY

# Count the number of .zip files in the specified directory and its subdirectories
echo "Counting .zip files in gs://forgood-temp-storage/rag_bench/swe/$DIRECTORY and its subdirectories:"
gsutil ls -r gs://forgood-temp-storage/rag_bench/swe/$DIRECTORY/** | grep '\.zip$' | wc -l
