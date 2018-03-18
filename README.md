# A Flask exercise for beginners

In this exercise, we will work with a CSV file as our data source to create individual pages for each of the 45 United States presidents. The CSV file is provided for you: *presidents.csv*

Our Flask app file is: *presidents.py*

A completed CSS file and 45 images have been provided in the *static* folder, which is where all such files (and JS files as well) must be for a Flask app to use them.

Three Flask template files are in the *templates* folder, also required for a Flask app that uses templates.

**NOTE:** It is assumed you are in a Python 3.6 virtual environment which has been activated and in which Flask has been installed.

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

To access any item inside a dictionary, we use its **key**. Our keys in `presidents_list` include `'President'` and `'Birthplace'`. We **cannot** access the dictionary with `presidents_list['President']` because &mdash; remember &mdash; `presidents_list` is a LIST. So we access one item in the list and *then* the key inside that item: `presidents_list[0]['President']`.

Save the edited *presidents.py* file and run it in Terminal with:

```python
python presidents.py
```

In your web browser, type `localhost:5000/` in the address bar to launch the Flask web server and view the result of route `'/'`.

If your browser displayed "Welcome to the presidential Flask example!" and "George Washington, born in Westmoreland County, Virginia." &mdash; you have verified that you can access `presidents_list` from a route function. Review the function above to ensure you understand how it worked, because we're about to change it further.

## Create a directory page to generate detail pages

In our app, there will be two page types:

* First, a directory page listing all presidents by name, in the order of their presidency. Each name will be a link that opens a president's detail page.
* Second, the detail page. This will have the same layout and information for each president.

We will change the existing Flask route to create the directory page.

Our first change is to add a **template** to the function. We already import `render_template` at the top of our app script, so all that's needed is to change the return statement, which currently reads:

```python
return heading + test1 + test2
```

To this:

```python
return render_template('index.html', pairs=pairs_list, the_title="Presidents Index")
```

This means that instead of writing the variables `heading`, `test1` and `test2` directly into the browser window, Flask will get a template file named *index.html* and write its contents into the browser window. The `render_template` function here passes two variables to the template: `pairs_list` and `the_title`. We have not created `pairs_list` yet.

### Examine the first template

All Flask templates must be in the *templates* directory. Open the template named *index.html* and note the following within the HTML:

* The H1 element
* A P element
* A UL element
* One LI element inside the UL

The H1 and P elements have normal text in them. We can write anything in a template that we would write in any regular HTML file.

The UL element contains Jinja2 templating directives:

```html+jinja
{% for pair in pairs %}
...
{% endfor %}
```

Those two directives are the start and end of a Python for-loop. If this reminds you of PHP (written inside HTML) &mdash; yes, it's the same idea. Flask allows us to insert Jinja2 directives to run Python commands in a template file.

We loop over a list named `pairs`. Where is that list, and how did the template get access to it? We passed it to this template with `return render_template()`, covered above. We haven't yet written the code that creates `pairs_list`, but when we look at this for-loop, we can see what the list must contain:

```html+jinja
{% for pair in pairs %}
    <li><a href="/president/{{ pair[0] }}">{{ pair[1] }}</a></li>
{% endfor %}
```

The double curly braces will be filled differently each time the loop repeats.

What we're aiming for is a list of 45 presidents in which each line looks like this:

```html
<li><a href="/president/1">George Washington</a></li>
```

Each pair in the list needs to provide, first, the number of the presidency, and second, the full name of the president.

Let's return to the app file and write that into the route.

### Get the data needed for the directory page

In the route function in *presidents.py*, delete old code so that you're left with this:

```python
@app.route('/')
def index():
    # presidents_list[0]['President']
    # presidents_list[0]['Birthplace']

    return render_template('index.html', pairs=pairs_list, the_title="Presidents Index")
```

**Do not delete anything above or below the route function!**

We know we need two items of information for each president: the number of the presidency, and the full name of the president. Earlier, we got the name of the first president with `presidents_list[0]['President']`. We got his birthplace with `presidents_list[0]['Birthplace']`. We don't need his birthplace now, but we need to know which **key** to use to get the number of his presidency.

Look at the CSV file and see if you can find it.

.<br>
.<br>
.

It's the first column, labeled "Presidency," so the **key** in the dictionary will be `['Presidency']`.

We need to get all the numbers and names for all the presidents. Let's use a loop. Let's put all the numbers in one list, `ids_list`, and all the names in another list, `name_list`.

```python
ids_list = []
name_list = []
# fill one list with the number of each presidency and
# fill the other with the name of each president
for president in presidents_list:
    ids_list.append(president['Presidency'])
    name_list.append(president['President'])
```

If you're asking:
   * Why `president['Presidency']` and `president['President']`
   * instead of `presidents_list[0]['Presidency']` and `presidents_list[0]['President']`,
you need to think about what the loop does. It take each president's dictionary one by one, as `president`, from the list (`presidents_list`).

Now we have all the data we need for the directory page, but the *index.html* template must receive a list of pairs: `[(number, name),(number, name), ...]`

Here's how we make that list of pairs from two lists:

```python
pairs_list = zip(ids_list, name_list)
```

Because our CSV lists the presidents in order by their presidency, and we made a *list* of dictionaries from that CSV, we can be sure that they are in the order we want, starting at 1 and ending at 45.

The final route function:

```python
@app.route('/')
def index():
    ids_list = []
    name_list = []
    # fill one list with the number of each presidency and
    # fill the other with the name of each president
    for president in presidents_list:
        ids_list.append(president['Presidency'])
        name_list.append(president['President'])
        # zip() is a built-in function that combines lists
        # creating a new list of tuples
    pairs_list = zip(ids_list, name_list)
    return render_template('index.html', pairs=pairs_list, the_title="Presidents Index")
```

Save the edited *presidents.py* file and run it in Terminal with:

```python
python presidents.py
```

Or, if the server is still active in Terminal, just reload the window you opened earlier.

### Revisit the first template

Although it's fairly plain, our directory page does have some styles applied. It also has a title (visible in the browser tab). Open *index.html* in the *templates* folder and let's see how that got done.

```html+jinja
{% extends 'base.html' %}

{% block content %}
{% endblock %}
```

More Jinja2 directives! The first one tells Flask that *index.html* extends another template file, named *base.html*. The second and third directives surround the HTML content that is **inserted into** the HTML in *base.html*.

Open *base.html*. This is where we find the HEAD element, with the CSS file link, and the TITLE element. Note that the TITLE element is filled dynamically. How was the correct text inserted here?

We sent the text to *base.html* via *index.html* with `return render_template()` in the route function in *presidents.py*:

```python
return render_template('index.html', pairs=pairs_list, the_title="Presidents Index")
```

Note carefully the way it is formatted in *base.html*:

```html+jinja
<title>{{ the_title }}</title>
```

Another thing to note in *base.html* is that these two directives exactly match those in *index.html*:

```html+jinja
{% block content %}
{% endblock %}
```

You could set up multiple blocks, in which case additional blocks would need to be labeled something other than *content*.

A final note about template files, for now, is that the double curly braces contain a placeholder that will be replaced by text, as we saw in *index.html*:

```html+jinja
{% for pair in pairs %}
    <li><a href="/president/{{ pair[0] }}">{{ pair[1] }}</a></li>
{% endfor %}
```
