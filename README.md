<!-- @format -->

# Kanban-Board π

This project is an implementation of a Kanban Board created in Flask.

# Local Setup

- Make sure you have the necessary requirements installed and updated, mentioned in the requirements.txt file. If not, just to be sure, go to terminal and run command `pip install -r requirements.txt`.

# Local Development Run

- Simply run `python main.py` , it will initiate the flask app in development.

# Replit run

- Click on `main.py` and click button run
- The web app will be available

# Folder Structure

- `root` has the `kanaban.sqlite3` DB.
- `static` has the all css files and Images.
- `templates` has all the html template files.

```

β   main.py
β   kanaban.sqlite3
β   readme.md
|   models.py
β
|
β
ββββstatic
β       image
|       |  All Images
|        addcard.css
|        confirmation.css
|        dashboard.css
|        list_confirmation.css
|        sum.css
|        update_list.css
|        updatecard.css
|
|
|
|
β
ββββtemplates
β       add_cards.html
β       card_confirmation.html
β       dashboard.html
β       list_confirmation.html
β       Signin.html
β       signup.html
β       summary.html
|       updatecards.html
|       updateList.html
|
β
ββββ__pycache__
        app.cpython-310.pyc
        models.cpython-310.pyc
```
