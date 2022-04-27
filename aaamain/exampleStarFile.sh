#!/bin/sh
# Reecepbcups - start.sh script for servers. EULA Auto Accepted.
            
MEM_HEAP="500M"
JAR_FILE="Paper-VERSION.jar"
PORT=29000

JAVA_ARGS="-Dfile.encoding=utf-8 -Dcom.mojang.eula.agree=true"

while true; do
	java -Xms$MEM_HEAP -Xmx$MEM_HEAP $JAVA_ARGS --port $PORT -jar $JAR_FILE nogui
	echo "Restarting server in 5 seconds"
	sleep 4
	echo "Restarting..."
	sleep 1
done