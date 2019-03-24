#echo "{\"effect\": {\"name\": \"Knight rider\"}, \"command\": \"effect\", \"priority\": 128 }" | nc 192.168.0.15 19444
EFF="{\"effect\": {\"name\": \"$1\"}, \"command\": \"effect\", \"priority\": 0 }"
echo $EFF | nc 192.168.0.15 19444