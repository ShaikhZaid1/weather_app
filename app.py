# app.py - Weather Forecast App
# Created for learning Python development from scratch!
import streamlit as st
import requests
import os

# Try to load .env if it exists (for local development)
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass  # On Streamlit Cloud, use secrets instead

# Get API key from either .env or Streamlit secrets
API_KEY = os.getenv('OPENWEATHER_API_KEY') or st.secrets.get("OPENWEATHER_API_KEY", "")

# Configure the page
st.set_page_config(
    page_title="Weather App",
    page_icon="🌤️",
    layout="centered"
)

# App title
st.title("🌤️ Weather Forecast App")
st.write("Enter a city name to get the current weather information!")

# Add a divider
st.divider()

# Input field for city name
city = st.text_input(
    "City Name", 
    placeholder="e.g., London, Tokyo, New York",
    help="Enter any city name worldwide"
)

# Only run if user has entered a city
if city:
    # Construct the API URL
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    
    # Show a loading spinner while fetching data
    with st.spinner('Fetching weather data...'):
        # Make the API request
        response = requests.get(url)
    
    # Check if the request was successful (status code 200 means success)
    if response.status_code == 200:
        # Parse JSON response into Python dictionary
        data = response.json()
        
        # Extract weather data from the response
        temperature = data['main']['temp']
        feels_like = data['main']['feels_like']
        temp_min = data['main']['temp_min']
        temp_max = data['main']['temp_max']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        description = data['weather'][0]['description']
        wind_speed = data['wind']['speed']
        country = data['sys']['country']
        
        # Display success message
        st.success(f"📍 Weather in {city.title()}, {country}")
        
        # Main weather info in columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="🌡️ Temperature",
                value=f"{temperature}°C",
                delta=f"{temperature - feels_like:.1f}°C difference"
            )
        
        with col2:
            st.metric(
                label="💧 Humidity",
                value=f"{humidity}%"
            )
        
        with col3:
            st.metric(
                label="💨 Wind Speed",
                value=f"{wind_speed} m/s"
            )
        
        # Weather description
        st.info(f"**Current Conditions:** {description.title()}")
        
        # Additional details in expandable section
        with st.expander("📊 More Details"):
            detail_col1, detail_col2 = st.columns(2)
            
            with detail_col1:
                st.write(f"**Feels Like:** {feels_like}°C")
                st.write(f"**Min Temp:** {temp_min}°C")
                st.write(f"**Max Temp:** {temp_max}°C")
            
            with detail_col2:
                st.write(f"**Pressure:** {pressure} hPa")
                st.write(f"**Country Code:** {country}")
        
    elif response.status_code == 404:
        st.error("❌ City not found! Please check the spelling and try again.")
    elif response.status_code == 401:
        st.error("❌ Invalid API key. Please check your .env file.")
    else:
        st.error(f"❌ Error: Unable to fetch weather data (Status code: {response.status_code})")

# Footer with instructions
st.divider()
st.caption("💡 Tip: Try entering cities from different countries!")
st.caption("Built with Streamlit and OpenWeatherMap API")
