from flask import Flask
import threema_mm.settings

app = Flask(__name__)

import threema_mm.views
