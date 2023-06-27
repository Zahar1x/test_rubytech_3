from app.views import app
from app.models import db


if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
