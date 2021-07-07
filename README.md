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

<h1><u>Table of Contents</u></h1>
<ul>
<li><a href="#tech-stack">Tech Stack</a></li>
<li><a href="#Features">Features</a></li>
  <ul>
  <li><a href="#homepage">Home</a></li>
  <li><a href="#addBooks">Search for Books</a></li>
  <li><a href="#tbr">To Be Read</a></li>
  <li><a href="#bookRecs">Book Recs</a></li>
  </ul>
<li><a href="#instructions">Installation</a></li>
</ul>

## Features

A user can either create an account/log in using their Spotify premium account - which is authorized via Spotify's oAuth flow.

![login](https://media.giphy.com/media/iVadCUYD5cgST9KqhA/giphy.gif)
<img height="250" src="https://i.ibb.co/zJp0NJH/Screen-Shot-2021-07-07-at-11-04-23-AM.png" alt="Connectify Logo">

Using Geolocation API and Google Maps Javascript API, the user is able to see users in their area, mapped and listed via Connect page.

![connect map](https://media.giphy.com/media/paafF5u3T7EmW1spve/giphy.gif)

 The user's listening data is pulled from Spotify's API, creating a snapshot of the user's top tracks, artists, and recently played playlists.

![my profile](https://media.giphy.com/media/Ga8oMboFCL3SMAwcFD/giphy.gif)

The user can peruse through the profiles of local users and see comparison analysis of music taste similarities and differences. Profiles are bookmarkable, allowing the user to categorize bookmarks based on similarity analysis.

![other profile](https://media.giphy.com/media/6AfJ7iM51loKymS8yW/giphy.gif)
![bookmark](https://media.giphy.com/media/lMAKBzXpR9dMK2hdyM/giphy.gif)
Users can create playists based on user's they have bookmarked, opening opportunity to discover new music they may be interested in.

![create a playlist](https://media.giphy.com/media/J0YRRz5OglN1xT1aP5/giphy.gif)
![see playlist](https://media.giphy.com/media/yyUdjy0ElHVAuwszlE/giphy.gif)

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

## Usage

To start the application, run the following commands in your terminal.

```python
# if you would like to utilize test information to play with, run the following:

python3 -i seed_database.py

# starts up the server
python3 -i server.py
```

## Connectify 2.0

Some additional features and design factors I would like to add in the near future:
- add additional data points for comparison analysis feature (utilize track/artist metadata to build fuller music taste snapshot)
- add in messaging/commenting feature
- further develop out Connect page map (unify UI between map and list feature)
- improve geolocation feature

## Contributing

Pull requests are welcome. As I continue to build out features and improve UX/UI design of the app, feel free to comment or reach out with any suggestions, refactoring advice, or feature requests I can try and add to the application.

## About Me



## Lets Connect!

You can reach me here on [Github](https://github.com/njbsanchez/Connectify) or connect with me on [LinkedIn](https://www.linkedin.com/in/njbsanchez/) at njbsanchez.
