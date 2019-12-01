# MSUScheduleWatcher
A program that will repeatedly search schedule.msu.edu for you, notifying you if your requested classes are available.

When the program is finished, the user will be able to specify classes https://schedule.msu.edu. The program will continually
watch them, and alert the user via text message if a section becomes available. The program will support multiple alerts of any classes,
and will eventually have loadable configs, so that users can quickly setup their alerts whenever they open the program again.

I created this program so I could get into my courses at Michigan State University. Even though I am a junior, I can't get into many 
of the classes I absolutely need in order to graduate. Academic advisors dont always have enough time to dedicate to each student, and this program will help students find courses when direct help isn't available.

Personally, class overrides have never worked for me. MSU has an open seat notification system, but you have to get in a queue (which are usually very long, especially for popular classes), and the system only checks every 20 minutes.

I wanted to skip the line, and check more often than the open seat notification system - so I created this program.
It is currently a work in progress, but it's coming along quickly, and I suspect to finish very soon.
Updates will be posted here.

A work in progress. As of 11/27/19, Alerts are working great.
However, there is no user input.


11/29/19:
User input added. Users are able to update the refresh time of each alert. Users are able to specify multiple classes within a course, ie. STT 351 430 441

11/30/19:
Implemented text message alerts, which are off by default. For now, you have to use the update command to turn them on for each alert. Currently, you have to enter your phone number every time you run the program, which is slightly annoying, but I have a few solutions in mind. I'm not liking how cluttered the main.py file is becoming, so I'm going to want to clean it up. It's the user input that complicates things. I think next on the to-do list is to implement loadable/saveable config files.
