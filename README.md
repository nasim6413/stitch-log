# Stitch tracker
Database for tracking floss for cross-stitch/embroidery projects. Currently supports DMC to Anchor conversions.

# Commands
* **list**: returns list of current stock.
* **count**: returns count of items in stock.
* * **convert *brand* *number***: returns possible conversiosn for specified floss number.
* **search *brand* *number***: returns information for specified floss number (if in stock). If unavailable, will check if there are possible conversions into the other brand.
* **add *brand* *number***: adds entry to stock.
* **del *brand* *number***: deletes entry from stock.
