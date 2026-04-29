from web import create_application, open_local_browser


if __name__ == "__main__":
    flask_application = create_application()
    open_local_browser("http://127.0.0.1:5000")
    flask_application.run(debug=False, host="127.0.0.1", port=5000, use_reloader=False)
