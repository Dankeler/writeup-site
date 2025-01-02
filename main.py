from website import create_app
from flask_migrate import Migrate
from flask.cli import with_appcontext

app = create_app()

@app.cli.command('db_init')
@with_appcontext
def db_init():
    from flask_migrate import init
    init()

if __name__ == "__main__":
    app.run(debug=False)
