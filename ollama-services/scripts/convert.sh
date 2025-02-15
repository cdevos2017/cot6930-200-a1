#!/bin/bash

# Check if input model folder is provided
if [ -z "$1" ]; then
    echo "Usage: convert.sh <model_folder>"
    echo "Example: convert.sh deepseek/r1"
    echo "This will look for the model in /mnt/models/deepseek/r1"
    echo "and output to /mnt/dev/gguf_models/deepseek-r1.gguf"
    exit 1
fi

MODEL_PATH=$1
MODEL_NAME=$(basename "$MODEL_PATH" | tr '/' '-')

cd /llama.cpp

echo "Converting model from /models/input/$MODEL_PATH"
echo "Output will be saved as /models/output/${MODEL_NAME}.gguf"

python3 convert.py \
    --outfile "/models/output/${MODEL_NAME}.gguf" \
    --outtype q4_k_m \
    --model "/models/input/${MODEL_PATH}"

echo "Conversion complete. Output saved to /models/output/${MODEL_NAME}.gguf"