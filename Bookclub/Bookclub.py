# Import the app instance from the Bookclub package
from Bookclub import app

# Check if the script is being run directly (not imported)
if __name__ == '__main__':
    # Run the Flask application with debugging enabled
    app.run(debug=True)
