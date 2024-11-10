# Data collector #

The goal is to collect data from OpenDataSoft : https://data.opendatasoft.com/explore/dataset/prix-carburants-quotidien%40opendatamef/table/

## Conf ##

Configuration is set by collector.conf file in conf folder : 
- data_id : the ID of the file to query
- target_path : the path where the data will be written

## Bin ##

This folder contains 2 files : 
- get_data_new.sh : script to retrieve data from API in json format.
- run.sh : script that execute get_data.sh 

### Launch command of data collection ###

Launch commande: *bash run.sh*
