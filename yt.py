import feedparser
from xml.etree import ElementTree
import requests
import xmltodict
import json
import os, sys


data_file = "./video_data.txt"
subscription_file = "./subscription_manager"
# Stores each video as an object
class post:

    def __init__(self, title, channel, url, date, description):
        # Figure out how to extrapolate video as python variables from here
        self.title = title.strip()
        self.channel = channel
        self.url = "https://youtube.com/watch?v="+url
        self.date  = date[:10]+" "+ date[11:]
        self.description = description

    # > operatory overload, used for sorting by date
    def __gt__(self, other):
        return self.date > other.date
    def __str__(self):
        return "{:<5.5} {:25.25} | {:^45.45}".format(self.date[5:10],self.channel, self.title)
    # == operator overload, used for tracking where in a list a subscription has moved
    def __eq__(self, other):
        return self.title == other.title and self.channel == other.channel
    # write to file, used for storing already seen videos
    def write(self, out):
        out.write(self.title +"\n" + self.channel +"\n"+ self.url +"\n"+self.date+"\n")


# opens xml file and puts each channel in root
d = feedparser.parse(subscription_file)
root = ElementTree.fromstring(d['feed']['summary'])
subscriptions = list()

# open subscription cache to load old subscription list while waiting to download new subscriptions
old_subscriptions = list()
f = open(data_file,"r")
old_sub_len = int(f.readline())
for i in range(old_sub_len):

    # store each old subscription as a post
    old_title = f.readline().strip()
    old_channel = f.readline().strip()
    old_url = f.readline().strip()
    old_date = f.readline().strip()
    old_subscriptions.append(post(old_title,old_channel,old_url,old_date,
    "Please wait for new videos to load in order to view descriptions!\n"))
    if old_sub_len-i < 100:
        print("{:3} | ".format(old_sub_len-i),old_subscriptions[i])

# fetches all video information from each channel, parses each video as a post and adds it to
# subscription lists, then sorts the subscription
print("Fetching new posts...")
for channel in root:
    response = requests.get(channel.attrib['xmlurl'])
    ch_root = xmltodict.parse(response.content)
    author = ch_root['feed']['title']
    # skips over channels with no videos
    if not 'entry' in ch_root['feed']:
        continue
    # adds each post to subscriptions list
    for video in ch_root['feed']['entry']:
        subscriptions.append(post(video['title'],author,video['yt:videoId'],video['published'],video['media:group']['media:description']))
subs = sorted(subscriptions)


# writes updated sub feed to stdout and cache file
# finds location of last video in new sub feed to determine how many new videos were posted
l = len(subs)
f = open(data_file,"w")
f.write(str(len(subs))+"\n")
# If the latest cache subscription isn't in the current sub feed, there have been more than 600
# videos since. Mark new index as distance between the last video previously seen and it's current
# location in the updated feed to determine how many news posts there are
if old_subscriptions[-1] in subs:
    new_index = len(subs) - subs.index(old_subscriptions[-1]) -1
else:
    new_index = 618
for vid in subs:

    # notifies user of unseen uploads if they exist
    if l == new_index and not new_index == 0:
        print("\n",new_index,"new upload(s) found.\n")
    # prints out most recent 100 posts
    if l < 100:
        print("{:3} | ".format(l),vid)
    vid.write(f)
    l-=1
if new_index==0:
    print("\n No new uploads found.\n")
elif new_index > 617:
    print("\n Over 617 uploads found")
f.close()

# Asks user to play videos from feed until they decide to quit
while(True):
    i = input("Select a number [q to quit]:\n")

    # quits and clears screen if letter pressed
    if(i.isalpha()):
        sys.stderr.write("\x1b[2J\x1b[H")
        break
    # if number is selected, play corresponding video and print description
    print("\n"*30+"-"*30,"\n"+subs[-int(i)].description,"\n"+"-"*30)
    os.system("mpv --really-quiet " + subs[-int(i)].url)
    # once video done playing, reprint sub list
    l = len(subs)
    for vid in subs:
        if l < 100:
            print("{:3} | ".format(l),vid)
        l-=1
