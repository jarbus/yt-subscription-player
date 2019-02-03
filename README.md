# YouTube Subscription Fetcher

This is a command-line utility that parses a file of YouTube channels and posts their videos by time uploaded. A video can be selected to watch in MPV by entering it's corresponding number.

# Installation
1. `pip3 install feedparser requests xmltodict`
2. Go to [https://www.youtube.com/subscription_manager](https://www.youtube.com/subscription_manager) and click the export button at the bottom of the page. This should give you a file called `subscription_manager` which you then put into whatever directory this repo is cloned into.


Requires MPV. However, any player can be used if it can play a YT video via a URL by editing the command used at the bottom of the file.

# Usage
Cd into whatever director this is installed to, and run `python3 yt.py`. Enter a number corresponding to a video you would like to play to play it. Enter any letter to quit.


