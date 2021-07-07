<p align="center">
  <img width="200" src="https://i.ibb.co/CV47pR3/logo-point.png" alt="Connectify Logo">

</p>

<h1 align="center">
    Connectify
</h1>
<h3 align="center">
    A Music-Based Social Media App
</h3>

Connectify is a music-based social media app that allows you to see how your music taste compares to other music fanatics in your area! 

Connectify does this in 3 steps: Connects, Compares, and Creates. By connecting Spotify and providing geolocation,  users can flip through other listener profiles within distance, see comparison statistics based on a listener's top tracks/artists , and bookmark listeners for later reference. Bookmarks are then aggregated based on similarity, giving the user the option to create playlists based off local top tracks.

## Table of Contents

<ul>
<li><a href="#aboutme">About Me</a></li>
<li><a href="#features">Features</a></li>
  <ul>
  <li><a href="#login">Log In</a></li>
  <li><a href="#connect">Connect with Local Users (using Geolocation & Google Maps API)</a></li>
  <li><a href="#otherprofile">Interacting with Other Profiles</a></li>
  <li><a href="#create">Create and Save Playlists to Spotify</a></li>
  </ul>
<li><a href="#demo">Demo Video (Youtube)</a></li>
<li><a href="#intall">Installation</a></li>
<li><a href="#connect2">Connectify 2.0</a></li>
<li><a href="#contribute">Connectify 2.0</a></li>
<li><a href="#connectme">Connectify with Me!</a></li>
</ul>

<a name="features"></a>
## Features

<a name="login"></a>
<h3>Log In</h3>
A user can either create an account/log in using their Spotify premium account - which is authorized via Spotify's oAuth flow.

![login](https://media.giphy.com/media/iVadCUYD5cgST9KqhA/giphy.gif)
<img height="250" src="https://i.ibb.co/zJp0NJH/Screen-Shot-2021-07-07-at-11-04-23-AM.png" alt="Connectify Logo">

<a name="connect"></a>
<h3>Connect with Local Users</h3>
Using Geolocation API and Google Maps Javascript API, the user is able to see users in their area, mapped and listed via Connect page.

![connect map](https://media.giphy.com/media/paafF5u3T7EmW1spve/giphy.gif)

<a name="myprofile"></a>
<h3>User's Music Profile</h3>
The user's listening data is pulled from Spotify's API, creating a snapshot of the user's top tracks, artists, and recently played playlists.

![my profile](https://media.giphy.com/media/Ga8oMboFCL3SMAwcFD/giphy.gif)

<a name="otherprofile"></a>
<h3>Interacting with Other Profiles</h3>
The user can peruse through the profiles of local users and see comparison analysis of music taste similarities and differences. Profiles are bookmarkable, allowing the user to categorize bookmarks based on similarity analysis.

![other profile](https://media.giphy.com/media/6AfJ7iM51loKymS8yW/giphy.gif)
![bookmark](https://media.giphy.com/media/lMAKBzXpR9dMK2hdyM/giphy.gif)
Users can create playists based on user's they have bookmarked, opening opportunity to discover new music they may be interested in.

<a name="create"></a>
<h3>Create and Save Playlists to Spotify</h3>
![create a playlist](https://media.giphy.com/media/J0YRRz5OglN1xT1aP5/giphy.gif)
![see playlist](https://media.giphy.com/media/yyUdjy0ElHVAuwszlE/giphy.gif)

<a name="demo"></a>
## Demo

For a quick demonstration of Connectify, please click the image below - You should be sent to a youtube video that covers various features of the app.

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/s4K1UPxAdaM/0.jpg)](https://www.youtube.com/watch?v=s4K1UPxAdaM)


## Tech Stack

- Python backend
- PostgreSQL database
- SQLalchemy
- React
- Flask
- Jinja
- JQuery
- HTML
- CSS
- Bootstrap

<a name="install"></a>
## Installation

To get started, clone Connectify by pasting below into your terminal.

```bash
git clone https://github.com/njbsanchez/Connectify.git
```


Separately, create developer accounts for both Spotify and Google Maps Javascript API. Once obtained, create a secrets.sh file and input the following:

```bash
export SPOTIPY_CLIENT_ID=<client_id_here>
export SPOTIPY_CLIENT_SECRET=<client_secret_here>
export GOOGLE_CLIENT_KEY=<google_key_here>      #due to nature of Google's API, there is no need for a client secret key.
```
Once you have Connectify opened in your preferred code editor, create and activate your virtual environment.

```bash

virtualenv env
source env/bin/activate


```
Install dependencies by installing requirements.txt file.

```bash

pip3 install -r requirements.txt

```

Source your API keys by applying secrets.sh to your virtual environment.

```bash

source secrets.sh

```

To start the application, run the following commands in your terminal.

```python
# if you would like to utilize test information to play with, run the following:

python3 -i seed_database.py

# starts up the server
python3 -i server.py
```
<a name="connect2"></a>
## Connectify 2.0

Some additional features and design factors I would like to add in the near future:
- add additional data points for comparison analysis feature (utilize track/artist metadata to build fuller music taste snapshot)
- add in messaging/commenting feature
- further develop out Connect page map (unify UI between map and list feature)
- improve geolocation feature

<a name="contribute"></a>
## Contributing

Pull requests are welcome. As I continue to build out features and improve UX/UI design of the app, feel free to comment or reach out with any suggestions, refactoring advice, or feature requests I can try and add to the application.

<a name="aboutme"></a>
## About Me

"After completing her B.S. in Accounting at the University of San Francisco, Nicole began her career as an auditor at Deloitte. Hungry for the opportunity to build, she joined Pinterest as a Deals Program Manager on the Operational Excellence team, strengthening work flows for international sales teams and  establishing key foundations for the Annual Deals Program. Nicole found herself drawn to the excitement that came with each new product launch, especially the new tools that supported small businesses on the platform. In participating in bug bashes and volunteering for feature testing, she realized that she, too, could build these awesome tools, leading her to a new path in software engineering."

<a name="connectme"></a>
## Lets Connect!

You can reach me here on [Github](https://github.com/njbsanchez/Connectify) or connect with me on [LinkedIn](https://www.linkedin.com/in/njbsanchez/) at njbsanchez.
