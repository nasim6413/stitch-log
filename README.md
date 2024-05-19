# Stitch Tracker
Database for tracking floss for cross-stitch/embroidery projects. Currently only supports DMC to Anchor conversions.

# Usage
* `list` returns list of current stock.
* `count` returns count of items in stock.
* `convert <brand> <number>` returns possible conversiosn for specified floss number.

* `search <brand> <number>` returns information for specified floss number (if in stock). If unavailable, program will check if there are possible conversions into the other brand.
* `add <brand> <number>` adds entry to stock.
* `del <brand> <number>` deletes entry from stock.