from app import up, migrate, drop, app

if __name__ == '__main__':
    migrate()
    app.run(debug=True)
