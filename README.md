AirCnC Listings App

## [Demo Here](https://airbnbmilestoneproject.herokuapp.com/)

My 'AirCnC Listings' is a app wholly built up from the up with Flask, MongoDB and Python. It'll be a display of a mix of technology I have been taught so far from the course. My app will showcase how a cross-platform document-oriented database and an elite level programming language, [Python](https://www.python.org/), can be manipulated to create creative and simple apps for the web.

---

## UX

My idea stemmed upon users being able to create and store Aircnc listings efficiently.
My app is designed to allow would be visotors to create a user specific profile, therefore, user data is protected by user restrictions where only the user could edit or delete it from the database. From there users can create, store, manage and delete aircnc listings. Any visiter to the app may also leave a review if they have been to that specific aircnc.
With an application, users want quick responsive menus that make sense and one that has been included was a "My Listing" section to manage their stored aircnc listings. Aircnc's in general have many variables attached to it and if a registered user needs to update one of varibales associated with their listing, my app allows them to do so.

---

## User Stories

Reasons why Aircnc Listing was created.

> As a user I need a place where I can create and store aircnc listings.

> There are lots of aircnc magazines with listings in there but it's not easy to get my listings in there as it takes time and it's costly.

> There are many aircnc host sites, however they come with x amount of fees for storing, why can't I store my aircnc listings for free.

> I need an app where I can easily list any aircnc that I own and be able to access them at a moments notice to update or delete them.

---

## Wireframes

[Website concept](https://raw.githubusercontent.com/alexrem1/airbnb-milestone-project/master/static/wireframes/concept.jpg)

---

## Aircnc Features

I have used various Materialize features such as carousel. This is used with the intention of giving aircnc listing pages an attractive carousel of photos related to their aircnc.

The pickadate features allows users that add listings to choose a date they were verified by Aircnc that gives visitors more details about that user.

The select feature gives users of the site predetermined options on, for example, amenities that their aircnc may or may not have. Aswell as bed size options their aircnc provides.

Another feature which compliments a sleek and simple navigation is navbar. As well as a desktop navbar version, when on mobile this navbar now pops out from the side when clicked upon.

Tap Target feature allows a user to click on the target and see a pop up of useful information in a fun and interative way.

The form feature allows users to not only add a complex aircnc listing to the database but it also allows anyone to leave a review of any listed aircnc.

Another feature my website possesesses can register and log in users, this feature allows me to create user restrictions and view restrictions this enables me to add extra levels of security where needed to protect my database or user data.

### Features Left to Implement

- Search bar feature to search specifically for aircnc property, as well as, aircnc's created by a specific user
- Upload picture(s) of aircnc on 'add listing' section instead of generic photos

---

## Technologies Used

- [Python 3](https://www.python.org/download/releases/3.0/)
- [Flask 1.1.2](http://flask.pocoo.org/)
- [HTML5](https://en.wikipedia.org/wiki/HTML5)
- [Materialize](https://materializecss.com/)
- [JavaScript](https://www.javascript.com/)
- [jQuery](https://jquery.com/)
- [MongoDB](https://www.mongodb.com/)

---

## Testing

Most of the applications testing was done throughout the entirety of development, most of which was manual tests.

**Testing Flask** - Within my app I had flask's debugger set to

```python
debug=True
```

So if Flask ever encounters an error the application shows it and indicates what caused it to crash. It was therefore imperative for time constraints and ease of use to test my application for every piece of work I would complete. Each time an error occured I would become more familiar with the error and how to fix it, ultimately speeding up the accuracy of my work and reduction of errors.

---

**Testing Python** - Again, writing Python would be done in bursts and if it didn't show in the browser, I would know I had done something wrong.

---

**Testing Flask Views** - As I worked on my project, each bit of work would be saved and then run on the browser. Thanks to debug being set to

```python
debug=True
```

it would again indicate wether it was flask view error or not and I would know straight away if it was functional.

---

**Testing the database** - At first, putting my collections in order was the hardest part for me. As I was developing my app, which changed from time to time based upon what direction I wanted to take the website in, it became more apparent what worked and what did not. Through this process I knew as long as I had the correct Python code, pulling data from my database was quick and seamless.
Once this had been put into practice, devoloping the needed requirement (CRUD) was again quick and seamless.

---

**Testing CRUD**

**READ**
The most important thing was making sure that users could see the aircnc listings that I initially created in MongoDB. To do this I had created a home route and loaded the property collection within this route then passed the data to the view. I tested this manually on the front-end and this worked as intended which allowed me to move on.

**UPDATE**
Now my website is reading my property collection from MongoDB, I moved onto being able to edit and update these aircnc's. At first I initially created a edit_listing route which meant that anyone could edit and update an aircnc listing which worked as intended on the fron-end and MongoDB.
Then I decided to make a change to my website design which only allowed users who had created their own aircnc listing to edit and update it. I had to update my insert_listing to allow logged in users to be associated with the inserted aircnc listing aswell as update_listing route to make sure once a user edit and updates their listing, they don't then become unassociated. I tested by updating an already associated property and manually checking MongoDB to see that it was still associated. This important fuctionality is needed to show another route: user_listing which is user specific aircnc listings.

**DELETE**
A delete_listing route was created which would delete the associated aircnc property from the database. I tested this in the browser and after deleting the aircnc property, it would then redirect back to user_listing.

**CREATE**
Testing the create functionality involved countless aircnc form submissions to which would in turn test the route when creating a new aircnc listing and did work as intended.

After working out a bug that occured when adding user authentication to insert_listing, the test phase was completed

All CRUD functionality in my app is working as intended

---

**Authentication & Authorisation**
Within my app I need user and page restrictions and for that to happen, I needed user registration functionality. Registering with a username and password inserted into my user collection against user_id.

If a potential user then tried to register with an already registered username it would notify them of the existing user and they would either try again or not. This way, certain views and data are restricted and so user data is protected.
Password hashing was implemented using [flask-bcrypt](https://flask-bcrypt.readthedocs.io/en/latest/)

I restricted certain views via back-end python which will only show if a authorised user is logged in.

```python
def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        username = session["username"]
        if not username:
            return redirect(url_for("login"))

        user = mongo.db.user.find({"username": username})
        if not user:
            return redirect(url_for("login"))

        return fn(*args, **kwargs)

    return wrapper
```

I included this route with all views that I wanted to protect and if said user was not logged in or registered then this validation would fail and so redirect any user not logged in to the login page.

Using the Jinja template language, I restricted certain views with logic and applied restrictions around elements on the page.

```python
{% if session['username'] %}
{% else %} {% endif %}
```

So here I was able to check if `username` was in session and if they were then the said user was able to view certain elements within my app. Such as user listings and the ability to edit, delete and create listings.

---

**Responsiveness** - Materialize is a modern responsive front-end framework and didn't come across any responsiveness issues while continuosly testing my app in Chrome Developers tools.

From doing this I have been able to confidently say that my app is fully responsiveness across all devices.

---

**Browser compatibility**

My app will be fully functional across all major modern browsers. I have tested my app on the following browsers.

- [Chrome](https://www.google.com/chrome/)
- [Firefox](https://www.mozilla.org/en-GB/firefox/new/)
- [Opera](https://www.opera.com/)
- [IE Edge](https://www.microsoft.com/en-gb/windows/microsoft-edge)
- [Safari](https://support.apple.com/en_GB/downloads/safari)
- [Chrome Mobile](https://chrome.en.softonic.com/)

---

## Deployment

Getting my application ready for deployment consisted of the following: -

1. During development, .bashrc held all keys and secrets. For production, however, these were entered into Heroku's Config Vars.
2. Ensuring the applications requirements.txt is up-to-date.
   **The command to update requirements**
   `pip3 freeze --local > requirements.txt`
3. Set up the Procfile - _A Procfile is required by Heroku in order to tell the service worker what command to run for my application to start._
4. Set Flask's debugging to False.
5. Push all my latest production ready code to Heroku ready for deployment via Heroku's GitHub function where you can deploy from GitHub the production ready app.

**Upon successful deployment Heroku will give you the URL that is hosted your app**

### Expanding on my project

To get set up with a copy of my project you can do these multiple ways.

**Via GitHub** -

1. You can manually download locally to your machine and then upload to your preferred IDE.
2. Install the projects requirements.txt using `pip3 install -r requirements.txt`
3. You will need to update a few environment variables before we can run the app.
   1. `app.config["MONGO_DBNAME"] = "airbnb_revieww"`
   2. `app.config["MONGO_URI"] = os.getenv("MONGO_URI", "monogodb://localhost")`
   3. `app.config["SECRET_KEY"] = os.getenv("SECRET")`
4. Once the above steps are complete you can try run the application using `python3 app.py`

**Via the CLI** -

1. Clone my repo via Git using the following command `https://github.com/ShaneMuir/Milestone-4.git`
2. Install the projects requirements.txt using `pip3 install -r requirements.txt`
3. You will need to update a few environment variables before we can run the app.
   1. `app.config["MONGO_DBNAME"] = "airbnb_revieww"`
   2. `app.config["MONGO_URI"] = os.getenv("MONGO_URI", "monogodb://localhost")`
   3. `app.config["SECRET_KEY"] = os.getenv("SECRET")`
4. Once the above steps are complete you can try run the application using `python3 app.py`

## Credits

Credit is due to the following names. Thank you so much:

- Mentor **Sandeep Aggarwal**
- Youtuber **Pretty Printed**

### Media

- [cover2](https://unsplash.com/photos/xY4r7y-Cllo)
- [cover1](https://unsplash.com/photos/y3TWYaUj8Ew)
- [cover5](https://unsplash.com/photos/_kifxaMv2QY)
- [1](https://unsplash.com/photos/mt2QzllH814)
- [2](https://unsplash.com/photos/b87_egH5mos)
- [3](https://unsplash.com/photos/7450hH--84M)
- [4](https://unsplash.com/photos/xx0oSB1YxRE)
- [5](https://unsplash.com/photos/XbwHrt87mQ0)
- [logo & favicon](https://www.freelogodesign.org/)
