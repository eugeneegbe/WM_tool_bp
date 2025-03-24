from tool import app

if __name__ == '__main__':
    app_context = app.app_context()
    app_context.push()

    app.run(debug=True)

    app_context.pop()