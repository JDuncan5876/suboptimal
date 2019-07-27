from get_route import get_route
from record import record
from run import strip_text, analyze_image, say, take_picture, match_station
import time

request = record()
station = match_station(strip_text(request))
start, stop, n_stops = get_route("111 8th Ave New York", station)
matched_start = match_station(strip_text(start))
matched_stop = match_station(strip_text(stop))
say("You're going to take " + matched_start + " " + str(n_stops) + " stops to " + matched_stop)
for i in range(n_stops):
    time.sleep(5)
    expected_match = matched_start if i == 0 else matched_stop if i == n_stops-1 else None
    if expected_match is not None:
        station = ""
        while station != expected_match:
            image_path = take_picture()
            station = match_station(analyze_image(image_path))
            print(station)
    else:
        image_path = take_picture()
        station = match_station(analyze_image(image_path))
    say("This is " + station)
    if i == n_stops-1:
        say("You have arrived")
    else:
        say("You have {} stops til your destination".format(n_stops-i-1))
