# Script cycles

This file defines the time intervals between scripts being runs. These timings are defined assuming that you will be using cron to schedule your scripts.

## Official product pullers

Pulls products into the wiki mirror.

### AMD

Pulls new products and product updates via the offical AMD product specifications page.

Timing interval: Once every 8 hours.

### Intel

Pulls new products and product updates via the offical Intel Product API.

Timing interval: Once every 8 hours.

### NVIDIA

NVIDIA does not appear to have an official source for product pulling.

Timing interval: undefined.

## Mirror to wiki duplication

Writes new and updated products to the wiki via the OneOrZero_Bot wiki bot.

Timing interval: Twice an hour.

## Price tracking puller

Pulls pricing information for products in the wiki mirror.

### Amazon

Pulls product pricing via Amazon Marketing API.

### Ebay

Pulls ebay product pricing via scraping.

Timing interval: Defined based on months-since-launch-date inserted into an exponentially decaying function.

### reddit.com/r/buildapcsales

Pulls reddit listings from MongoDB store. The MongoDB store is filled with listings via the oshiro.py PRAW listener.

Timing interval: Twice an hour.

### Craigslist

Timing interval: Defined based on months-since-launch-date inserted into an exponentially decaying function.

### OfferUp

Timing interval: Defined based on months-since-launch-date inserted into an exponentially decaying function.

### Facebook Marketplace

Timing interval: Defined based on months-since-launch-date inserted into an exponentially decaying function.

### NewEgg

Timing interval: Defined based on months-since-launch-date inserted into an exponentially decaying function.

## Microcenter

