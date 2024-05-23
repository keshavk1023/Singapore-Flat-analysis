import pandas as pd  # Importing the pandas library for data manipulation and analysis
import numpy as np  # Importing the numpy library for numerical operations
import warnings  # Importing the warnings library to manage warnings
import streamlit as st  # Importing the streamlit library to create web apps
from streamlit_option_menu import option_menu  # Importing a specific component from streamlit for creating option menus
import pickle  # Importing the pickle library to serialize and deserialize Python objects
import os  # Importing the os library for interacting with the operating system

# Suppress warnings
warnings.filterwarnings("ignore")  # Ignoring all warnings

# Set working directory
os.chdir("C:\\Users\\jeetg\\code\\flat")  # Changing the current working directory

# Define constants for min/max values
MIN_FLOOR_AREA = 31  # Minimum floor area in square meters
MAX_FLOOR_AREA = 280  # Maximum floor area in square meters
MIN_STOREY_START = 1  # Minimum starting storey
MAX_STOREY_END = 50  # Maximum ending storey
MIN_REMAINING_LEASE_YEAR = 42  # Minimum remaining lease years
MAX_REMAINING_LEASE_YEAR = 97  # Maximum remaining lease years
MIN_REMAINING_LEASE_MONTH = 0  # Minimum remaining lease months
MAX_REMAINING_LEASE_MONTH = 11  # Maximum remaining lease months

# Mapping functions
def map_input(value, mapping_dict, value_name):  # Function to map input values using a dictionary
    mapped_value = mapping_dict.get(value, -1)  # Get the mapped value from the dictionary
    if mapped_value == -1:  # If the value is not found
        st.error(f"Invalid input for {value_name}. Please check your inputs.")  # Display an error message
    return mapped_value  # Return the mapped value

def town_mapping(town):  # Function to map town names to numerical values
    town_dict = {  # Dictionary to map town names to numbers
        'ANG MO KIO': 0, 'BEDOK': 1, 'BISHAN': 2, 'BUKIT BATOK': 3, 'BUKIT MERAH': 4,
        'BUKIT PANJANG': 5, 'BUKIT TIMAH': 6, 'CENTRAL AREA': 7, 'CHOA CHU KANG': 8,
        'CLEMENTI': 9, 'GEYLANG': 10, 'HOUGANG': 11, 'JURONG EAST': 12, 'JURONG WEST': 13,
        'KALLANG/WHAMPOA': 14, 'MARINE PARADE': 15, 'PASIR RIS': 16, 'PUNGGOL': 17,
        'QUEENSTOWN': 18, 'SEMBAWANG': 19, 'SENGKANG': 20, 'SERANGOON': 21, 'TAMPINES': 22,
        'TOA PAYOH': 23, 'WOODLANDS': 24, 'YISHUN': 25
    }
    return map_input(town, town_dict, "town")  # Return the mapped town value

def flat_type_mapping(flat_type):  # Function to map flat types to numerical values
    flat_type_dict = {  # Dictionary to map flat types to numbers
        '1 ROOM': 0, '2 ROOM': 1, '3 ROOM': 2, '4 ROOM': 3, '5 ROOM': 4,
        'EXECUTIVE': 5, 'MULTI-GENERATION': 6
    }
    return map_input(flat_type, flat_type_dict, "flat type")  # Return the mapped flat type value

def flat_model_mapping(flat_model):  # Function to map flat models to numerical values
    flat_model_dict = {  # Dictionary to map flat models to numbers
        '2-room': 0, '3Gen': 1, 'Adjoined flat': 2, 'Apartment': 3, 'DBSS': 4,
        'Improved': 5, 'Improved-Maisonette': 6, 'Maisonette': 7, 'Model A': 8,
        'Model A-Maisonette': 9, 'Model A2': 10, 'Multi Generation': 11,
        'New Generation': 12, 'Premium Apartment': 13, 'Premium Apartment Loft': 14,
        'Premium Maisonette': 15, 'Simplified': 16, 'Standard': 17, 'Terrace': 18,
        'Type S1': 19, 'Type S2': 20
    }
    return map_input(flat_model, flat_model_dict, "flat model")  # Return the mapped flat model value

# Prediction function
def predict_price(year, town, flat_type, flr_area_sqm, flat_model, stry_start, stry_end, re_les_year, re_les_month, les_coms_dt):  # Function to predict the price of a flat
    # Validate inputs
    town = town_mapping(town)  # Map town input to numerical value
    flat_type = flat_type_mapping(flat_type)  # Map flat type input to numerical value
    flat_model = flat_model_mapping(flat_model)  # Map flat model input to numerical value

    if town == -1 or flat_type == -1 or flat_model == -1:  # Check if any input mapping failed
        return None  # Return None if any input is invalid

    # Transform inputs
    year = int(year)  # Convert year to integer
    flr_area_sqm = int(flr_area_sqm)  # Convert floor area to integer
    stry_start = np.log(int(stry_start))  # Apply logarithm transformation to storey start
    stry_end = np.log(int(stry_end))  # Apply logarithm transformation to storey end
    re_les_year = int(re_les_year)  # Convert remaining lease year to integer
    re_les_month = int(re_les_month)  # Convert remaining lease month to integer
    les_coms_dt = int(les_coms_dt)  # Convert lease commence date to integer
    
    with open("Resale_Flat_Prices_Model_1.pkl", "rb") as f:  # Open the model file in read-binary mode
        reg_model = pickle.load(f)  # Load the model using pickle

    user_data = np.array([[year, town, flat_type, flr_area_sqm, flat_model, stry_start, stry_end, re_les_year, re_les_month, les_coms_dt]])  # Create an array of user inputs
    user_data = user_data.clip(min=0)  # Clip negative values to 0
    y_pred = reg_model.predict(user_data)  # Predict the price using the model
    price = np.exp(y_pred[0])  # Exponentiate the predicted value to get the price

    return round(price)  # Return the rounded price

# Streamlit configuration
st.set_page_config(layout="wide")  # Set the layout of the Streamlit app to wide
st.title(":red[Singapore Resale Flat Prices Prediction]")  # Set the title of the app

# Sidebar menu
with st.sidebar:  # Create a sidebar
    select = option_menu("MAIN MENU", ["Home", "Price Prediction", "About"])  # Add a menu with options

# Home section
if select == "Home":  # If the 'Home' option is selected
    st.header(":orange[HDB Flats]")  # Add a header
    st.write("The majority of Singaporeans live in public housing provided by the Housing and Development Board. HDB flats can be purchased either directly from the HDB as a new unit or through the resale market from existing owners.")  # Add a description
    st.header(":orange[Resale Process]")  # Add a header
    st.write("In the resale market, buyers purchase flats from existing flat owners, and the transactions are facilitated through the HDB resale process. The process involves a series of steps, including valuation, negotiations, and the submission of necessary documents.")  # Add a description
    st.header(":orange[Valuation]")  # Add a header
    st.write("The HDB conducts a valuation of the flat to determine its market value. This is important for both buyers and sellers in negotiating a fair price.")  # Add a description
    st.header(":orange[HDB Loan and Bank Loan]")  # Add a header
    st.write("Buyers can choose to finance their flat purchase through an HDB loan or a bank loan. HDB loans are provided by the HDB, while bank loans are obtained from commercial banks.")  # Add a description
    st.header(":orange[Market Trends]")  # Add a header
    st.write("The resale market is influenced by various factors such as economic conditions, interest rates, and government policies. Property prices in Singapore can fluctuate based on these factors.")  # Add a description
    st.header(":orange[Online Platforms]")  # Add a header
    st.write("There are online platforms and portals where sellers can list their resale flats, and buyers can browse available options.")  # Add a description

# Price Prediction section
elif select == "Price Prediction":  # If the 'Price Prediction' option is selected
    st.header("Predict Resale Flat Prices")  # Add a header
    st.write(":orange[Enter the details below to get the predicted resale price of an HDB flat.]")  # Add a description

    col1, col2 = st.columns(2)  # Create two columns
    with col1:  # In the first column
        year = st.selectbox("Select the Year", [str(i) for i in range(2015, 2025)], help="Year of the resale transaction.")  # Create a dropdown for selecting the year
        town = st.selectbox("Select the Town", ['ANG MO KIO', 'BEDOK', 'BISHAN', 'BUKIT BATOK', 'BUKIT MERAH',
                                                'BUKIT PANJANG', 'BUKIT TIMAH', 'CENTRAL AREA', 'CHOA CHU KANG',
                                                'CLEMENTI', 'GEYLANG', 'HOUGANG', 'JURONG EAST', 'JURONG WEST',
                                                'KALLANG/WHAMPOA', 'MARINE PARADE', 'PASIR RIS', 'PUNGGOL',
                                                'QUEENSTOWN', 'SEMBAWANG', 'SENGKANG', 'SERANGOON', 'TAMPINES',
                                                'TOA PAYOH', 'WOODLANDS', 'YISHUN'], help="Town where the flat is located.")  # Create a dropdown for selecting the town
        flat_type = st.selectbox("Select the Flat Type", ['1 ROOM', '2 ROOM', '3 ROOM', '4 ROOM', '5 ROOM', 'EXECUTIVE', 'MULTI-GENERATION'], help="Type of the flat.")  # Create a dropdown for selecting the flat type
        flr_area_sqm = st.number_input(f"Enter the Floor Area (sqm) (Min: {MIN_FLOOR_AREA} / Max: {MAX_FLOOR_AREA})", min_value=MIN_FLOOR_AREA, max_value=MAX_FLOOR_AREA, help="Floor area of the flat in square meters.")  # Create a number input for entering the floor area
        flat_model = st.selectbox("Select the Flat Model", ['2-room', '3Gen', 'Adjoined flat', 'Apartment', 'DBSS', 'Improved', 'Improved-Maisonette', 'Maisonette', 'Model A', 'Model A-Maisonette', 'Model A2', 'Multi Generation', 'New Generation', 'Premium Apartment', 'Premium Apartment Loft', 'Premium Maisonette', 'Simplified', 'Standard', 'Terrace', 'Type S1', 'Type S2'], help="Model of the flat.")  # Create a dropdown for selecting the flat model

    with col2:  # In the second column
        stry_start = st.number_input(f"Enter the Storey Start (Min: {MIN_STOREY_START})", min_value=MIN_STOREY_START, max_value=MAX_STOREY_END, help="Starting storey of the flat.")  # Create a number input for entering the starting storey
        stry_end = st.number_input(f"Enter the Storey End (Min: {stry_start})", min_value=stry_start, max_value=MAX_STOREY_END, help="Ending storey of the flat.")  # Create a number input for entering the ending storey
        re_les_year = st.number_input(f"Enter the Remaining Lease Year (Min: {MIN_REMAINING_LEASE_YEAR} / Max: {MAX_REMAINING_LEASE_YEAR})", min_value=MIN_REMAINING_LEASE_YEAR, max_value=MAX_REMAINING_LEASE_YEAR, help="Remaining lease years of the flat.")  # Create a number input for entering the remaining lease years
        re_les_month = st.number_input(f"Enter the Remaining Lease Month (Min: {MIN_REMAINING_LEASE_MONTH} / Max: {MAX_REMAINING_LEASE_MONTH})", min_value=MIN_REMAINING_LEASE_MONTH, max_value=MAX_REMAINING_LEASE_MONTH, help="Remaining lease months of the flat.")  # Create a number input for entering the remaining lease months
        les_coms_dt = st.selectbox("Select the Lease Commence Date", [str(i) for i in range(1966, 2023)], help="Year the lease commenced.")  # Create a dropdown for selecting the lease commence date

    button = st.button("Predict the Price")  # Create a button for predicting the price

    if button:  # If the button is clicked
        pre_price = predict_price(year, town, flat_type, flr_area_sqm, flat_model, stry_start, stry_end, re_les_year, re_les_month, les_coms_dt)  # Call the predict_price function with the user inputs
        if pre_price:  # If a price is predicted
            st.write(f"## :green[*The Predicted Price is:*] ${pre_price}")  # Display the predicted price
        else:  # If no price is predicted
            st.write(f"## :red[*Prediction could not be made due to invalid inputs. Please check and try again.*]")  # Display an error message

# About section
elif select == "About":  # If the 'About' option is selected
    st.header("About This App")  # Add a header
    st.write("This application predicts the resale prices of HDB flats in Singapore using a pre-trained machine learning model. Enter the required details in the 'Price Prediction' section to get the predicted price of a resale flat.")  # Add a description
    st.header("About Me")  # Add a header
    Name = (f'{"Name :"}  {"KESHAV KUMAR"}')  # Create a variable for the name
    mail = (f'{"Mail :"}  {"keshavkumar.1023@gmail.com"}')  # Create a variable for the email
    social_media = {  # Dictionary for social media links
        "GITHUB": "https://github.com/keshavk1023",
        "LINKEDIN": "www.linkedin.com/in/keshav-kumar-8075a5185"}

    st.subheader(Name)  # Display the name
    st.subheader(mail)  # Display the email

    st.write("#")  # Add a line break
    cols = st.columns(len(social_media))  # Create columns for social media links
    for index, (platform, link) in enumerate(social_media.items()):  # Iterate through the social media links
        cols[index].write(f"[{platform}]({link})")  # Display the social media links
