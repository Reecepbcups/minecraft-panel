### Stress Test A Server
```
git clone https://github.com/PureGero/minecraft-stress-test.git
cd minecraft-stress-test && mvn

# Ensure your server.properties is the following:
online-mode=false
allow-flight=true

# protocol version: https://wiki.vg/Protocol_version_numbers
java -Dbot.protocol.version=758 -Dbot.ip=127.0.0.1 -Dbot.port=25678 -Dbot.radius=1000 -Dbot.count=1000 -jar target/minecraft-stress-test-1.0.0-SNAPSHOT-jar-with-dependencies.jar
```