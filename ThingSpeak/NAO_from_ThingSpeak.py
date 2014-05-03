""" A simple example to test if NAO can get data from thingspeak.com.

"""

from naoqi import ALProxy
import httplib, urllib
import time


# NAO_IP = "mistcalf.local"
#NAO_IP = "192.168.0.13"

tts = ALProxy("ALTextToSpeech", NAO_IP, 9559)

def main():
    tts.say("I'm going to get some data from the internet now!")
    
    # use your API key generated in the thingspeak channels for the value of 'key'
    # nb Different API key to read.
    conn = httplib.HTTPConnection("api.thingspeak.com:80")
    channel_id = 12012
    field_id = "NAO_1"
    url = "/channels/" + str(channel_id) + "/feeds.json?results=5"
    print "url: ", url
    try:
        conn.request("GET", url)
        response = conn.getresponse()
        print response.status, response.reason
        data = response.read()
        print data
        conn.close()
    except:
            print "connection failed"
            
    tts.say("I got some stuff from the internet!")   
    
    
if __name__ == "__main__":
    main()