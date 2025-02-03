import streamlit as st
import serpapi
import json
from groq import Groq
import os
from datetime import datetime, timedelta
from typing import List, Dict
from dotenv import load_dotenv

# Set page configuration to wide mode
st.set_page_config(layout="wide", page_title="Flight Search & Analysis", page_icon="✈️")

# Custom CSS for better styling
st.markdown("""
    <style>
        .stApp {
            background-color: #f5f7f9;
        }
        .main {
            padding: 2rem;
        }
        .st-emotion-cache-1y4p8pa {
            padding: 2rem;
            border-radius: 1rem;
            background-color: white;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .st-emotion-cache-16idsys p {
            font-size: 1.1rem;
            color: #1f1f1f;
        }
        .st-expander {
            background-color: white;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
            border: 1px solid #e0e0e0;
        }
    </style>
""", unsafe_allow_html=True)

# Load environment variables and initialize client (same as before)
load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ"))


# Keep the existing helper functions
def search_flights(departure_id: str, arrival_id: str, outbound_date: str,
                   return_date: str, currency: str, adults: str) -> Dict:
    params = {
        "api_key": os.getenv("SERP_API_KEY"),
        "engine": "google_flights",
        "hl": "en",
        "gl": "us",
        "departure_id": departure_id,
        "arrival_id": arrival_id,
        "outbound_date": outbound_date,
        "return_date": return_date,
        "currency": currency,
        "adults": adults,
    }
    return serpapi.search(params)


def extract_flight_info(json_data: Dict) -> List[Dict]:
    # Keep the existing implementation
    all_flights = []
    for flight_category in ['best_flights', 'other_flights']:
        if flight_category in json_data:
            for flight_option in json_data[flight_category]:
                flight_info = {
                    'price': flight_option['price'],
                    'total_duration': flight_option['total_duration'],
                    'flights': []
                }

                for flight in flight_option['flights']:
                    flight_segment = {
                        'flight_number': flight['flight_number'],
                        'travel_class': flight['travel_class'],
                        'departure_airport': {
                            'name': flight['departure_airport']['name'],
                            'id': flight['departure_airport']['id'],
                            'time': flight['departure_airport']['time']
                        },
                        'arrival_airport': {
                            'name': flight['arrival_airport']['name'],
                            'id': flight['arrival_airport']['id'],
                            'time': flight['arrival_airport']['time']
                        },
                        'duration': flight['duration']
                    }
                    flight_info['flights'].append(flight_segment)

                if 'layovers' in flight_option:
                    flight_info['layovers'] = [
                        {
                            'duration': layover['duration'],
                            'airport': layover['name']
                        }
                        for layover in flight_option['layovers']
                    ]
                else:
                    flight_info['layovers'] = []

                all_flights.append(flight_info)
    return all_flights


def get_groq_analysis(flights: List[Dict], preferences: str) -> str:
    # Keep the existing implementation
    flight_description = json.dumps(flights, indent=2)
    prompt = f"""
    Analyze these flight options based on the following user preferences: {preferences}

    Flight data:
    {flight_description}

    Please provide:
    1. Top 3 recommended flights based on the preferences
    2. Pros and cons for each recommendation
    3. Overall best choice with justification
    """

    chat_completion = groq_client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a flight recommendations expert who analyzes flight options based on user preferences."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.5,
        max_completion_tokens=1024,
        top_p=1,
    )
    return chat_completion.choices[0].message.content


def main():
    # Header section with custom styling
    st.markdown("""
        <h1 style='text-align: center; color: #1e3d59; margin-bottom: 2rem;'>
            ✈️ Smart Flight Search & Analysis
        </h1>
    """, unsafe_allow_html=True)

    # Container for the main content
    with st.container():
        # Search form with improved styling
        with st.form("flight_search", clear_on_submit=False):
            st.markdown("### Search Parameters")

            # Create three columns for better layout
            col1, col2, col3 = st.columns([1, 1, 1])

            with col1:
                st.markdown("##### Departure Details")
                departure_id = st.text_input("From (Airport Code)", "CDG")
                outbound_date = st.date_input("Departure Date",
                                              min_value=datetime.now().date(),
                                              value=datetime.now().date() + timedelta(days=1))

            with col2:
                st.markdown("##### Arrival Details")
                arrival_id = st.text_input("To (Airport Code)", "AUS")
                return_date = st.date_input("Return Date",
                                            min_value=outbound_date,
                                            value=outbound_date + timedelta(days=7))

            with col3:
                st.markdown("##### Additional Options")
                currency = st.selectbox("Currency", ["USD", "EUR", "GBP"])
                adults = st.number_input("Number of Adults", min_value=1, value=1)

            # Preferences section
            st.markdown("### Travel Preferences")
            preferences = st.text_area(
                "",
                "Example: I prefer shorter flights with minimal layovers and am willing to pay more for comfort.",
                height=100
            )

            # Center the submit button
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                submitted = st.form_submit_button("🔍 Search Flights",
                                                  use_container_width=True)

    if submitted:
        # Results section
        with st.spinner("🔄 Searching for available flights..."):
            search_results = search_flights(
                departure_id, arrival_id,
                outbound_date.strftime("%Y-%m-%d"),
                return_date.strftime("%Y-%m-%d"),
                currency, str(adults)
            )
            flights = extract_flight_info(search_results)

            # Display results in two columns
            col1, col2 = st.columns([2, 1])

            with col1:
                st.markdown("### 📋 Available Flights")
                for i, flight in enumerate(flights, 1):
                    with st.expander(
                            f"Flight Option {i} - ${flight['price']:,.2f} | Duration: {flight['total_duration']} min"
                    ):
                        for j, segment in enumerate(flight['flights'], 1):
                            st.markdown(f"""
                                #### ✈️ Segment {j}
                                - **Flight**: {segment['flight_number']} ({segment['travel_class']})
                                - **Departure**: {segment['departure_airport']['name']} ({segment['departure_airport']['id']})
                                - **Time**: {segment['departure_airport']['time']}
                                - **Arrival**: {segment['arrival_airport']['name']} ({segment['arrival_airport']['id']})
                                - **Time**: {segment['arrival_airport']['time']}
                                - **Duration**: {segment['duration']} minutes
                            """)

                        if flight['layovers']:
                            st.markdown("#### 🛑 Layovers")
                            for layover in flight['layovers']:
                                st.markdown(f"- **{layover['airport']}**: {layover['duration']} minutes")

            with col2:
                st.markdown("### 🤖 AI Analysis")
                with st.spinner("Analyzing your options..."):
                    analysis = get_groq_analysis(flights, preferences)
                    st.markdown(analysis)


if __name__ == "__main__":
    main()