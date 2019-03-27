# rainmachine-amweather
Personal weather station parser from the Ambient Weather Network for the RainMachine sprinkler controller.

This parser was thrown together over a Sunday morning to feed data from an AMbient Weather PWS
into a RainMachine. I pretty much never use Python, so if this isn't quite right, that's why. I wanted something
that would pull data from my weather station without having to rely on WUnderground. You can still use WUnderground
too but now you have two sources in case either one decides to change something or has a problem.

Every Ambient Weather PWS that's capable of uploading to ambientweather.net is identified by its MAC address.
You'll also need an API Key and Application Key, which you can create at https://dashboard.ambientweather.net/account
All three of those things are needed to use this parser.

### Developed using:
* WS-2000 with Osprey sensor array
* ambientweather.net account
* RainMachine HD-16 (second gen), firmware v4.0.974

### LICENSE: GNU General Public License v3.0

GitHub: https://github.com/WillCodeForCats/rainmachine-amweather

### Quick and Dirty Setup
Upload the parser to your RainMachine at Settings -> Weather the click "Add New". It will appear under the
"User Uploaded" tab where you can configure the keys and MAC address.

If there's a problem check under About -> VIEW LOG and see if there's an error. It logs as "user-ambientweather-parser".

## FUTURE WORK
Ambient Weather does have a LAN-based receiver, which at some point I may look into how to poll data directly
from that and avoid any reliance on "the cloud" or internet access. But until that happens the ambientweather.net
API is required. I'm not a huge fan of doing everything "in the cloud" for various reasons (privacy, exposure, etc.),
so a LAN-only option is interesting to me.
