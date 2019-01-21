# Servicebeat
Servicebeat fetches installed services, check if they are in running state and ships them to Elasticsearch or Logstash.

## Getting started
After downloading Heracles, you need to configure ''servicebeat.yml'' file in order to use it. 

services - list of service names to monitor, if values is ''*'' then all installed services will be taken

schedule - interval in seconds for shipping data

## Install