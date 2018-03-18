# Flask exercise

In this exercise, we will work with a CSV file as our data source to create individual pages for each of the 45 United States presidents. The CSV file is provided for you: *presidents.csv*

Our Flask app file is: *presidents.py*

A completed CSS file and 45 images have been provided in the *static* folder, which is where all such files (and JS files as well) must be for a Flask app to use them.

Three Flask template files are in the *templates* folder, also required for a Flask app that uses templates.

## Convert a CSV file to a dictionary

Our first task is to convert the CSV to a Python dictionary (or more accurately, a list of dictionaries).

A function to do this has already been written. It is in the *modules.py* file. It requires the built-in Python module `csv`.

```python
import csv

def convert_to_dict(filename):
    """
    Convert a CSV file to a list of Python dictionaries.
    """
    # open a CSV file - note - must have column headings in top row
    datafile = open(filename, newline='')

    # create list of OrderedDicts as of Python 3.6
    my_reader = csv.DictReader(datafile)

    # write it all out to a new list
    list_of_dicts = []
    for row in my_reader:
        # we convert each row to a string and add a newline
        list_of_dicts.append( dict(row) )

    # close original csv file
    datafile.close()
    # return the list
    return list_of_dicts
```

Instead of copying this function into our Flask app file, *presidents.py*, we will **import** it there. Add this on line 2:

```python
from modules import convert_to_dict
```

Note that now you can run `convert_to_dict()` by entering any CSV filename as the argument. The function returns a list of dictionaries. With *presidents.csv* as the argument, the function returns a list of 45 dictionaries. Add this on line 5, *above* the route:

```python
presidents_list = convert_to_dict("presidents.csv")
```

It is convenient to have `presidents_list` as a global variable so that we can use it in all of our Flask routes.

## Test the dictionary list in a Flask route

The Flask app (*presidents.py*) already has one simple route:

```python
@app.route('/')
def index():
    return '<h1>Welcome to the presidential Flask example!</h1>'
```

In *presidents.py*, change the route function `index()` to:

```python
def index():
    heading = '<h1>Welcome to the presidential Flask example!</h1>'
    test1 = '<p>' + presidents_list[0]['President']
    test2 = ", born in " + presidents_list[0]['Birthplace'] + '.</p>'
    return heading + test1 + test2
```

We know that `listname[0]` will return the value of the **first item** in a Python list. In our list of dictionaries, `presidents_list`, each item is a complete dictionary of information about one U.S. president.

To access items inside a dictionary, we use the **key**. Our keys in `presidents_list` include `'President'` and `'Birthplace'`. We **cannot** access the dictionary with `presidents_list['President']` because &mdash; remember &mdash; `presidents_list` is a LIST. So we access one item in the list and *then* the key inside that item: `presidents_list[0]['President']`.

Save the edited *presidents.py* file and run it in Terminal with:

```python
python presidents.py
```

**NOTE:** It is assumed you are in a Python 3.6 virtual environment which has been activated and in which Flask has been installed.

In your web browser, type `localhost:5000/` in the address bar to launch the Flask web server and view the result of route `'/'`.
