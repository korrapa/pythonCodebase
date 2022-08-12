import sys

# add your project directory to the sys.path
project_home = '/home/lakshmanpythonapps/Inventory_Module'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# import flask app but need to call it "application" for WSGI to work
from inventory import app as application  # noqa


if __name__ == "__main__":
        application.run()