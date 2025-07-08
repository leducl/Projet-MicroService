from app import create_app
import os
if __name__ == "__main__":
    port = int(os.getenv('PORT', 5002))
    app = create_app()
    app.run(host='0.0.0.0', port=port)
