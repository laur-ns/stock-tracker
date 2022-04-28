# Investment portfolio manager

The purpose of this assignment is to help me understand networks at a lower level.

Things I learned:
Socket programming, deploying to cloud, greater familiarity with python, BASIC authentication, docker, web servers

#

[Heroku main page link](https://stock-159.herokuapp.com/)

Will not work without proper API key:

[Portfolio](https://stock-159.herokuapp.com/portfolio)

[Research](https://stock-159.herokuapp.com/research)

## Notes:

- The username and password are both `21011877`.
- The portfolio validates all input except for the symbol name (too many symbols to compare against). If invalid symbol is entered, it will attempt to place it in the JSON file and likely return an error.
- The api key is out of credits and needs to be replaced (replace the API_KEY variable at the top of the server.py program).
- The chart used is from Google charts.

## How to run the program locally:

Make sure python 3 is installed. On the terminal, make sure it is at the current directory and type:

```Python3
pip install requests
```

Then:

```Python3
python server.py {port_number}
```

Set `port_number` to any free port (e.g. 8080)

If successful, the webserver can be accessed at `localhost:{port_number}`.
