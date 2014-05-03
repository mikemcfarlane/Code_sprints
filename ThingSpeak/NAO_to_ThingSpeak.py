""" A simple example to test if NAO can connect to thingspeak.com.

"""

from naoqi import ALProxy
import httplib, urllib
import time

# NAO_IP = "mistcalf.local"
NAO_IP = "192.168.0.13"

tts = ALProxy("ALTextToSpeech", NAO_IP, 9559)

def main():
    tts.say("I'm going to connect to the internet now!")
    
    for i in range (5):
        params = urllib.urlencode({'field1': i, 'key':'9PBYIQ1RWXJ6XZBO'})     # use your API key generated in the thingspeak channels for the value of 'key'
        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = httplib.HTTPConnection("api.thingspeak.com:80")                
        try:
            conn.request("POST", "/update", params, headers)
            response = conn.getresponse()
            print i, msg
            print response.status, response.reason
            data = response.read()
            conn.close()
        except:
                print "connection failed"
        tts.say("I sent some stuff to the internet!")
        # If using ThingSpeak web service there is a 15s limit. Install locally or on own webserver for faster usage.
        time.sleep(16)
    
    tts.say("Yay, all sent!")
    
    
if __name__ == "__main__":
    main()