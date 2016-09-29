import RPi.GPIO as GPIO

ledB = 27
ledG = 22
ledR = 10

GPIO.setmode(GPIO.BCM)
GPIO.setup(ledG, GPIO.OUT)
GPIO.setup(ledR, GPIO.OUT)
GPIO.setup(ledB, GPIO.OUT)

def cleanLed():
    GPIO.output(ledG, True)
    GPIO.output(ledR, True)
    GPIO.output(ledB, True)

def redLed():
    GPIO.output(ledR, False)

def blueLed():
    GPIO.output(ledB, True)

def greenLed():
    GPIO.output(ledG, True)

# make_server is used to create this simple python webserver
from wsgiref.simple_server import make_server

# Function that is ran when a http request comes in
def simple_app(env, start_response):

    # set some http headers that are sent to the browser
    status = '200 OK'
    headers = [('Content-type', 'text/html')]
    start_response(status, headers)

    # What did the user ask for?
    if env["PATH_INFO"] == "/r":
        print("user asked for /on")
        cleanLed()
        redLed()
        return '<!DOCTYPE html>'\
                '<html>'\
                    '<head>'\
                        '<title>"Lights"</title>'\
                    '</head>'\
                    '<body>'\
                        '<a title="Red" href="/r">Red</a>'\
                        '<a title="Green" href="/g">Green</a>'\
                        '<a title="Blue" href="/b">Blue</a>'\
                    '</body>'\
                '</html>'

    elif env["PATH_INFO"] == "/g":
        print("user asked for /off")
        cleanLed()
        greenLed()
        return '<!DOCTYPE html>'\
                '<html>'\
                    '<head>'\
                        '<title>"Lights"</title>'\
                    '</head>'\
                    '<body>'\
                        '<a title="Red" href="/r">Red</a>'\
                        '<a title="Green" href="/g">Green</a>'\
                        '<a title="Blue" href="/b">Blue</a>'\
                    '</body>'\
                '</html>'

    elif env["PATH_INFO"] == "/b":
        print("user asked for /off")
        cleanLed()
        blueLed()
        return '<!DOCTYPE html>'\
                '<html>'\
                    '<head>'\
                        '<title>"Lights"</title>'\
                    '</head>'\
                    '<body>'\
                        '<a title="Red" href="/r">Red</a>'\
                        '<a title="Green" href="/g">Green</a>'\
                        '<a title="Blue" href="/b">Blue</a>'\
                    '</body>'\
                '</html>'

    else:
        print("user asked for something else")
        return '<!DOCTYPE html>'\
                '<html>'\
                    '<head>'\
                        '<title>"Lights"</title>'\
                    '</head>'\
                    '<body>'\
                        '<a title="Red" href="/r">Red</a>'\
                        '<a title="Green" href="/g">Green</a>'\
                        '<a title="Blue" href="/b">Blue</a>'\
                    '</body>'\
                '</html>'

# Create a small python server
httpd = make_server("", 8011, simple_app)
print "Serving on port 8011..."
print "You can open this in the browser http://192.168.1.xxx:8011 where xxx is your rpi ip aadress"
print "Or if you run this server on your own computer then http://localhost:8011"
httpd.serve_forever()
