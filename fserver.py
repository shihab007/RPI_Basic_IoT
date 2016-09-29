import RPi.GPIO as GPIO

ledB = 27
ledG = 22
ledR = 10

GPIO.setmode(GPIO.BCM)
GPIO.setup(ledG, GPIO.OUT)
GPIO.setup(ledR, GPIO.OUT)
GPIO.setup(ledB, GPIO.OUT)

GPIO.output(ledG, True)
GPIO.output(ledR, True)
GPIO.output(ledB, True)

# make_server is used to create this simple python webserver
from wsgiref.simple_server import make_server

# Function that is ran when a http request comes in
def simple_app(env, start_response):
    
    # set some http headers that are sent to the browser
    status = '200 OK'
    headers = [('Content-type', 'text/html')] 
    start_response(status, headers)

    # What did the user ask for?
    if env["PATH_INFO"] == "/on":
        print("user asked for /on")
	GPIO.output(ledB, False)
	GPIO.output(ledG, False)
	GPIO.output(ledR, False)
	return "<html><body>got on<p><a href=\"/off\">Turn off</a></body></html>"
	
    elif env["PATH_INFO"] == "/off":
        print("user asked for /off")
	GPIO.output(ledB, True)
	GPIO.output(ledR, True)
	GPIO.output(ledG, True)
	return "<html><body>got off <p><a href=\"/on\">Turn me on</a></body></html>"
    else:
        print("user asked for something else")
	return "<html><body><a href=\"/on\">Turn me on</a></body></html>"            

# Create a small python server
httpd = make_server("", 8011, simple_app)
print "Serving on port 8011..."
print "You can open this in the browser http://192.168.1.xxx:8011 where xxx is your rpi ip aadress"
print "Or if you run this server on your own computer then http://localhost:8011" 
httpd.serve_forever()
