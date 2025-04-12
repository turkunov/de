#!/bin/bash

OUTPUT_FILE="output.txt"
rm -f $OUTPUT_FILE



spark2-submit solution_df.py > /dev/null


if [ -f "$OUTPUT_FILE" ]; then
    cat $OUTPUT_FILE
    rm $OUTPUT_FILE
else
    echo "Error: Spark job did not produce $OUTPUT_FILE" >&2 
    # Or simply: exit 1
    exit 1
fi