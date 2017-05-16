import http.client
import curses
import time
import json
import sys

#from pprint import pprint
def main(screen) :
    youtubeApiKey = """(enter your api key here)"""

    numberOfSystemArguments = len(sys.argv) - 1

    channelName = "UCMYUDLNxMvqxgjYc4tGwaow"

    i = 0
    while i < numberOfSystemArguments:
        if sys.argv[i] == "--channel" :
            channelName = sys.argv[i + 1]
            i = i + 1
        i = i + 1

    youtubeConnection = http.client.HTTPSConnection("www.googleapis.com")
    requestForm = "/youtube/v3/channels?part=statistics&id={}&key={}".format(channelName, youtubeApiKey);
    frame = 50
    sampleNumber = 0
    while(1):
        screen.nodelay(True)
        input = screen.getch()
        if input == ord('q') :
            break

        if frame == 50 :
            youtubeConnection.request("GET", requestForm)
            request = youtubeConnection.getresponse()

            screen.addstr(23, 0, "Last Request status: {} {}".format(request.status, request.reason))

            channelPageHtml = request.read()
            dataAll = json.loads(channelPageHtml.decode("utf-8"));
            dataStatistics = dataAll["items"][0]["statistics"]

            screen.addstr(0, 0, "Number of Subscribers: {} @ SampleNumber: {}".format(dataStatistics["subscriberCount"], sampleNumber))
            frame = 0
            sampleNumber = sampleNumber + 1

        screen.refresh()
        time.sleep(0.01)
        frame = frame + 1
        
curses.wrapper(main)
