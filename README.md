# Ge-data

## Purpose
This project was made to gather market data for the economy of Oldschool Runescape (OSRS). Initially the system was
built to gather data from the official OSRS API (which provides fairly inaccurate data and only updates once a day) 
and from the Osbuddy ge database (an API of a formerly popular 3rd party client for OSRS). 

Later functions to email users when the OSRS database prices were updated were added, as well
as methods for gathering data from the rs wiki, which offers data gathered with
the another 3rd party client called Runelite.

In order to enrich the limited data from the official API I have resorted to scraping the official webpage which
contains more accurate data in the source. This function is automatically started when an update to the OSRS API is detected.

## Installation
**Instructions will follow**

## Usage
Schedule script with function call in crontab. I personally ran this script off a
raspberry pi. 
