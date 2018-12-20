import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_cors import CORS
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from webapp import app, db

from user import models

CORS(app)

app.config.from_object('webapp.config.HerokuConfig')

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)
manager.add_command('runserver',
                    Server(
                        use_debugger=True,
                        use_reloader=True,
                        host=os.getenv('IP', '0.0.0.0'),
                        port=int(os.getenv('PORT', 5000))
                    ))

if __name__ == '__main__':
    manager.run()
