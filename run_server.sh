#!/bin/bash
# Script to build and run the Scopa Game Server

echo "====================================="
echo "Building Scopa Game Server..."
echo "====================================="

cd "$(dirname "$0")"

# Compile the server
mvn clean compile

if [ $? -eq 0 ]; then
    echo ""
    echo "====================================="
    echo "Starting Game Server on port 5000..."
    echo "====================================="
    echo ""
    
    # Run the server
    mvn exec:java -Dexec.mainClass="com.example.scopa.server.GameServer"
else
    echo "Build failed!"
    exit 1
fi
