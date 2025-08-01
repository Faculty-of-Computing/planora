from db import create_tables
from init import app
import routes as _

create_tables()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
