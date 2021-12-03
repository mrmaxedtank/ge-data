# Ge-data

## The project
This project was made to gather market data for the economy of Oldschool Runescape (OSRS). Initially the system was
built to gather data from the official OSRS API (which provides fairly inaccurate data and only updates once a day) 
and from the Osbuddy ge database (an API of a formerly popular 3rd party client for OSRS). 

Later functions to email users when the OSRS database prices were updated were added, as well
as methods for gathering data from the rs wiki, which offers data gathered with
the another 3rd party client called Runelite.

In order to enrich the limited data from the official API I have resorted to scraping the official webpage which
contains more accurate data in the source. This function is automatically started when an update to the OSRS API is detected.

I used to run a scheduled query over the gathered dataset and pushed the results to a webpage of mine where I presented the data using datatables. This system still exists and functions well, and while I don't use the data any longer, I do store compressed copies of all the jsons this script gathers in the cloud, in case I decide to analyse a bigger dataset at a later time. 

## Installation
Using sql script in the db folder to recreate my database structure and use crontab after to schedule the different parts of the script, using the different possible arguments. Personally I:
1) Run the script with argument --osrs once a minute.
2) Run the script with argument --osb once every 10 minutes (this API is (nowadas) fairly inactive and only supplies fresh data twice an hour, normally)
3) Run the script with argument --wiki every 5 minutes.
4) Run the script with argument --enrichment_check every hour. This function scrapes the itemdb webpage to get more accurate data and add this to the data that came from the official OSRS API. 

The following other arguments are possible:
- --initialize: launches the initial setup: rebuilds the limits table and queries the APIs to start building the dataset.
- --rebuild: rebuilds the limits table using the osrsbox API.
- --enrich: forces the script to check if there are lines in the OSRS API table that require enrichment, and if those exist the script will enrich the lines.
- --updated: launch the script in a way to pretend the OSRS API was updated.  

**Note:** the table ge.items is not provided and will need to be build by hand (of with your own query). While I no longer use the data I gather with this system, I don't feel comfortable sharing the collection of items I earned in-game money with.

## Usage
Schedule script with function call in crontab. I personally ran this script off a
raspberry pi. 
