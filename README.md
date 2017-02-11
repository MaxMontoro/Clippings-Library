## Clippings Library

Organize your Kindle clippings in the browser.

Uses Flask and an underlying sqlite database.

## Usage

Coming soon, I promise.

        $ export FLASK_APP=clippings.py
        $ initdb
        $ flask run
        
Visit `http://0.0.0.0:8001/addall` to add all entries to the database.
Then visit `http://0.0.0.0:8001/` to see the homepage.