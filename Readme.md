#StockDbSync
A simple python3 package to slurp all the data from the yahoo CSV api
and keep it in a local Postgres database.  It uses the DjangoORM internally.

Only the NASDAQ is built in to sync in the package, but anything you can fetch
by symbol name from Yahoo should work (as long as you get the symbol names right).

It takes a considerable amount of time for initial run.  Staying synced is meant
to be run as a background task via cron or whatever, not a watch and wait.  Printing
output is just so you know the script hasn't stalled on something.

**Scripts**  
Browse the scripts folder to see example creation of the database and where
the package stores configuration data.

**Examples**  
There's really only one example.  It's in the module's example folder...

**djangoORM**
It's not tracked in this repo, because it exists in one of my other
github repos.
