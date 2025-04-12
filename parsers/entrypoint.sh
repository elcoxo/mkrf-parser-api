#!/bin/bash
echo "[START] Data parsing has started and may take a while. Data is being added incrementally, but you can already access it via the API."
if python main.py; then
  echo "[DONE] All data has been uploaded to the database :)"
else
  echo "[ERROR] Data parsing failed. Check the logs above for details."
  exit 1
fi
