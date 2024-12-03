from HSA import app

# from livereload import Server

if __name__ == '__main__':
    # server = Server(app.wsgi_app)
    # server.serve(debug=app.config['DEBUG'], port=app.config['PORT'])
    app.run(debug=app.config['DEBUG'], port=app.config['PORT'])
