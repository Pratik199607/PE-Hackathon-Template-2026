from app import create_app
from app.core.logger import setup_logger
setup_logger()
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
