from get_route import get_route
from speech import get_speech
from run import strip_text, analyze_image, say, take_picture, match_station
import time

audio_file = "/Users/jared/Downloads/audio.raw" # TODO record
request = get_speech(audio_file)
if len(request) == 0:
    say("Sorry, I didn't quite get that")
station = match_station(strip_text(request))
start, stop, n_stops = get_route("111 8th Ave New York", station)
matched_start = match_station(strip_text(start))
matched_stop = match_station(strip_text(stop))
say("You're going to take " + start + " to " + stop)
for i in range(n_stops):
    time.sleep(5)
    expected_match = matched_start if i == 0 else matched_stop if i == n_stops-1 else None
    if expected_match is not None:
        station = ""
        while station != expected_match:
            image_path = take_picture()
            station = match_station(analyze_image(image_path))
        say("This is " + station)
    else:
        image_path = take_picture()
        station = match_station(analyze_image(image_path))
    say("This is " + station)
    if i == n_stops - 1:
        say("You have arrived")
    else:
        say("You have {} stops til your destination".format(n_stops-i-1))