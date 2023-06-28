from WebServer.Service.webServer import  app
from WebServer.Config.config import CONFIG

WEBSITE_HOST = CONFIG.website_host
WEBSITE_PORT = CONFIG.website_port

def run():
    app.run(host=WEBSITE_HOST, 
            port=WEBSITE_PORT, 
            debug=False)