# Stitch Tracker
Database for tracking floss for cross-stitch/embroidery projects.

# Usage
* `help` returns list of available commands.
* `list` returns list of current stock.
* `count` returns number of items in stock.
* `convert <brand> <number>` returns possible conversions for specified floss number.
* `search <brand> <number>` returns information for specified floss number (if in stock). If unavailable, will return any possible conversions into the other brand (if in stock).
* `add <brand> <number>` adds entry to stock.
* `del <brand> <number>` deletes entry from stock.