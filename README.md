# Suboptimal

Suboptimal is a New York Subway station guide for the impaired.

For the blind, a microphone broadcasts the station name.
For the deaf, the name of the subway station is displayed on screen.

## Motivation

There are 2849 trains built before 2000 (starting from 1964).
Representing 44.3% of all active trains serving the 5.5 million daily customer's of the MTA.
These trains don't broadcast clear announcements on subway stations. It becomes difficult to know which subway station you're arriving at without clearer cues.

## How it works

Suboptimal is a Raspberry Pi with a camera, speaker and screen module. Using a optical character recognition Machine Learning Google Cloud vision API, we analyze images taken by the Pi as you sit on the subway.
Upon matching text on signs to known subway station names, the module both speaks the name and displays it on screen for you.