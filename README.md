# Web Scraper

Python tool to scrape websites directly or through a cron job for a particular string and get notified when a new relevant item is added on a webpage.

Sample settings file (required):

    http://forums.hardwarezone.com.sg/graphics-display-bazaar-200/
    1060

After first run with **scraper.py**, each additional run throws notification to user if new objects are found. To install CRON job on UNIX systems to auto-check every 5 minutes, run **install.sh**

## Prerequisites:
- BeatifulSoup 4
- notify2
- urllib2
- requests
