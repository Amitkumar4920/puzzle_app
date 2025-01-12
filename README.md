I want to build a Python application that converts Excel files to HTML while maintaining the Excel table structure. The application should map Excel column names and date formats to predefined rules provided in a Markdown file. Additionally, the application should be tested thoroughly within a virtual environment. Test it by placing an Excel file in an input folder, processing it, and saving the converted HTML in an output folder. Ensure error handling and debugging to correct any issues during development.



# Puzzle Game

A Python-based puzzle game with a web interface.

## Features

- Interactive puzzle game interface
- Flask web server backend
- Test suite for game logic
- Responsive web design

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your browser and navigate to `http://localhost:5000`

## Project Structure

- `app.py` - Main Flask application
- `puzzle_game.py` - Core game logic
- `test_app.py` - Test suite
- `templates/` - HTML templates
- `requirements.txt` - Project dependencies
