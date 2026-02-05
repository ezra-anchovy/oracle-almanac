#!/bin/bash
cd "$(dirname "$0")"
echo "Oracle Almanac available at http://localhost:8888"
python3 -m http.server 8888
