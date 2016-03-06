import os
from application import app

port = int(os.environ.get("PORT", 5000))
app_api.run(host='0.0.0.0', port=port)
