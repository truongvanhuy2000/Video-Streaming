from webServer.service.webServer import  app

def run():
    app.run(host="0.0.0.0", debug=False)