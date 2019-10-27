# Infant Videos
Note that this is where you would place all video you would like 
to play during scan. Videos should go in a folder that is the 
same name as your particpant (_e.g._ **./Pilot01**). This is 
case sensitive.

The start of videos are time locked to the start of volume 
acquisition. The current time length for each video is set 
for 12 seconds.

This means if your video is longer than 12 seconds, it will 
be truncated at 12s. If your video is shorter than 12 seconds, 
it will be truncated at the largest multiple of the repetition 
time. (Currently set at TR = 1s)