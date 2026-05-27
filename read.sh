#!/usr/bin/env

SOURCE_DIR="/mnt/seagate/workspace/coding/projetos/scripts/copykit/src"
OUTPUT_FILE="$HOME/Desktop/copycat.txt"

# limpa o arquivo de saída antes de começar
> "$OUTPUT_FILE"

find "$SOURCE_DIR" -type f -name "*.py" | sort | while read -r file; do
    echo "--- $file ---" >> "$OUTPUT_FILE"
    cat "$file" >> "$OUTPUT_FILE"
    echo -e "\n" >> "$OUTPUT_FILE"
done