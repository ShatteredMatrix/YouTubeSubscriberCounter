import http.client
import curses
import time
import sys

def getSubscribersNumber(channelPageHtml):
    pattern = """<span class="yt-subscription-button-subscriber-count-branded-horizontal subscribed yt-uix-tooltip" """
    channelPageHtmlString = channelPageHtml.decode("utf-8")
    pos = channelPageHtmlString.find(pattern);

    #print (channelPageHtmlString)
    #print (pos)

    i = pos;
    while channelPageHtmlString[i] != '>' :
        i = i + 1
    i = i + 1
    subscribers = 0
    #while int(channelPageHtmlString[i]) >= int('0') and int(channelPageHtmlString[i]) <= int('9'):
    while channelPageHtmlString[i] != '<' :
        if channelPageHtmlString[i] != '.' :
            subscribers = subscribers * 10 + int(channelPageHtmlString[i])
        i = i + 1
    return subscribers

numberOfSystemArguments = len(sys.argv) - 1

channelName = "/channel/UCMYUDLNxMvqxgjYc4tGwaow/"

i = 0
while i < numberOfSystemArguments:
    if sys.argv[i] == "--channel" :
        channelName = sys.argv[i + 1]
        i = i + 1
    i = i + 1

screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)

youtubeConnection = http.client.HTTPSConnection("www.youtube.com")
frame = 50
sampleNumber = 0
while(1):
    screen.nodelay(True)
    input = screen.getch()
    if input == ord('q') :
        break

    if frame == 50 :
        youtubeConnection.request("GET", channelName)
        request = youtubeConnection.getresponse()
        #print (request.status, request.reason)
        screen.addstr(1, 0, "{} {}".format(request.status, request.reason))

        channelPageHtml = request.read()

        #print (getSubscribersNumber(channelPageHtml))
        screen.addstr(0, 0, "Number of Subscribers: {} @ SampleNumber: {}".format(getSubscribersNumber(channelPageHtml), sampleNumber))
        frame = 0
        sampleNumber = sampleNumber + 1

    screen.refresh()
    time.sleep(0.01)
    frame = frame + 1

curses.nocbreak()
screen.keypad(False)
curses.echo()
curses.endwin()
