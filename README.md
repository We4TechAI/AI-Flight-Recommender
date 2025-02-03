# AI Flight Recommender 🛫

![AI Flight Recommender Banner](banner.png)

A smart flight search and recommendation system that combines real-time flight data with AI-powered analysis to help users find their ideal flights based on personal preferences.

## Features ✨

- Real-time flight search using Google Flights data
- AI-powered flight analysis and recommendations
- Customizable search parameters
- Interactive user interface
- Multi-currency support
- Layover analysis
- Detailed flight segment information
- Personalized recommendations based on preferences

## Prerequisites 📋

Before running the application, make sure you have:

- Python 3.8+
- SerpAPI API key
- Groq API key
- Docker (optional, for containerized deployment)

## Installation 🚀

### Local Installation

1. Clone the repository:
```bash
git clone https://github.com/We4TechAI/AI-Flight-Recommender.git
cd AI-Flight-Recommender
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:
```env
SERP_API_KEY=your_serpapi_key_here
GROQ=your_groq_api_key_here
```

### Docker Installation

1. Build the Docker image:
```bash
docker build --tag ai_flight_recommender:latest .
```

2. Run the container:
```bash
docker run -d --name ai_flight_recommender -p 8501:8501 ai_flight_recommender:latest
```

## Usage 📖

1. Start the application:
   - Local: `streamlit run main.py`
   - Docker: Access through `http://localhost:8501`

2. Enter flight search parameters:
   - Departure airport code
   - Arrival airport code
   - Travel dates
   - Number of passengers
   - Currency preference

3. Specify your travel preferences in the text area (e.g., "I prefer morning flights with minimal layovers")

4. Click "Search Flights" to get results and AI analysis

## Project Structure 📁

```
AI-Flight-Recommender/
├── main.py              # Main application file
├── Dockerfile          # Docker configuration
├── requirements.txt    # Python dependencies
├── .env               # Environment variables
├── banner.png         # Project banner
└── README.md          # Project documentation
```

## Environment Variables 🔐

Create a `.env` file with the following variables:

```env
GROQ=your_groq_api_key_here
SERPAPI_KEY=your_serpapi_key_here
```

## Docker Support 🐳

The application can be containerized using Docker. The included Dockerfile sets up the environment and runs the Streamlit application.

### Build Image
```bash
docker build --tag ai_flight_recommender:latest .
```

### Run Container
```bash
docker run -d --name ai_flight_recommender -p 8501:8501 ai_flight_recommender:latest
```

## API Documentation 📚

### SerpAPI
- Used for fetching real-time flight data
- Documentation: [SerpAPI Google Flights](https://serpapi.com/google-flights-api)

### Groq
- Used for AI-powered flight analysis
- Documentation: [Groq API](https://console.groq.com/docs/quickstart)

## Contributing 🤝

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push to branch: `git push origin feature/new-feature`
5. Submit a pull request

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments 🙏

- SerpAPI for flight data
- Groq for AI capabilities
- Streamlit for the UI framework

## Support 💬

For support, please open an issue in the GitHub repository or contact the maintainers.
