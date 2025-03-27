# Java Forum Stuttgart 2025 Conference Viewer

A web application to browse talks, speakers and keywords for the Java Forum Stuttgart 2025 conference.

## Features

- View all conference talks with filtering by topic, language and level
- Detailed talk view with abstract, speaker info and keywords  
- Speaker profiles with biography and contact information
- Keyword cloud visualization showing popular topics
- Responsive design works on mobile and desktop

## Technologies Used

- Python 3
- Flask web framework
- Bootstrap 5 for responsive UI
- Jinja2 templating
- Vanilla JavaScript for client-side filtering

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/java-forum-stuttgart-2025.git
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the development server:
```bash
python app.py
```

The app will be available at `http://localhost:5000`

## Data Structure

The app expects two JSON files in the `data/` directory:
- `10_2025_speakers_import.json` - Speaker information
- `20_2025_talks_import.json` - Talk information

## Screenshots

![Talk List](static/img/screenshot-talks.png)
![Speaker Profile](static/img/screenshot-speaker.png)
![Keyword Cloud](static/img/screenshot-keywords.png)

## License

MIT License
