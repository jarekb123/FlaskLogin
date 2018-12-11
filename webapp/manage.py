from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from webapp.app import app, db
from user import models

app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

# if __name__ == '__main__':
#     manager.run()

