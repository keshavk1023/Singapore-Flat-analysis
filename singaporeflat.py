import pandas as pd
import numpy as np
import warnings
import streamlit as st
from streamlit_option_menu import option_menu
import pickle
import os

# Suppress warnings
warnings.filterwarnings("ignore")

# Set working directory
os.chdir("C:\\Users\\jeetg\\code\\flat")

# Define constants for min/max values
MIN_FLOOR_AREA = 31
MAX_FLOOR_AREA = 280
MIN_STOREY_START = 1
MAX_STOREY_END = 50
MIN_REMAINING_LEASE_YEAR = 42
MAX_REMAINING_LEASE_YEAR = 97
MIN_REMAINING_LEASE_MONTH = 0
MAX_REMAINING_LEASE_MONTH = 11

# Mapping functions
def map_input(value, mapping_dict, value_name):
    mapped_value = mapping_dict.get(value, -1)
    if mapped_value == -1:
        st.error(f"Invalid input for {value_name}. Please check your inputs.")
    return mapped_value

def town_mapping(town):
    town_dict = {
        'ANG MO KIO': 0, 'BEDOK': 1, 'BISHAN': 2, 'BUKIT BATOK': 3, 'BUKIT MERAH': 4,
        'BUKIT PANJANG': 5, 'BUKIT TIMAH': 6, 'CENTRAL AREA': 7, 'CHOA CHU KANG': 8,
        'CLEMENTI': 9, 'GEYLANG': 10, 'HOUGANG': 11, 'JURONG EAST': 12, 'JURONG WEST': 13,
        'KALLANG/WHAMPOA': 14, 'MARINE PARADE': 15, 'PASIR RIS': 16, 'PUNGGOL': 17,
        'QUEENSTOWN': 18, 'SEMBAWANG': 19, 'SENGKANG': 20, 'SERANGOON': 21, 'TAMPINES': 22,
        'TOA PAYOH': 23, 'WOODLANDS': 24, 'YISHUN': 25
    }
    return map_input(town, town_dict, "town")

def flat_type_mapping(flat_type):
    flat_type_dict = {
        '1 ROOM': 0, '2 ROOM': 1, '3 ROOM': 2, '4 ROOM': 3, '5 ROOM': 4,
        'EXECUTIVE': 5, 'MULTI-GENERATION': 6
    }
    return map_input(flat_type, flat_type_dict, "flat type")

def flat_model_mapping(flat_model):
    flat_model_dict = {
        '2-room': 0, '3Gen': 1, 'Adjoined flat': 2, 'Apartment': 3, 'DBSS': 4,
        'Improved': 5, 'Improved-Maisonette': 6, 'Maisonette': 7, 'Model A': 8,
        'Model A-Maisonette': 9, 'Model A2': 10, 'Multi Generation': 11,
        'New Generation': 12, 'Premium Apartment': 13, 'Premium Apartment Loft': 14,
        'Premium Maisonette': 15, 'Simplified': 16, 'Standard': 17, 'Terrace': 18,
        'Type S1': 19, 'Type S2': 20
    }
    return map_input(flat_model, flat_model_dict, "flat model")

# Prediction function
def predict_price(year, town, flat_type, flr_area_sqm, flat_model, stry_start, stry_end, re_les_year, re_les_month, les_coms_dt):
    # Validate inputs
    town = town_mapping(town)
    flat_type = flat_type_mapping(flat_type)
    flat_model = flat_model_mapping(flat_model)

    if town == -1 or flat_type == -1 or flat_model == -1:
        return None

    # Transform inputs
    year = int(year)
    flr_area_sqm = int(flr_area_sqm)
    stry_start = np.log(int(stry_start))
    stry_end = np.log(int(stry_end))
    re_les_year = int(re_les_year)
    re_les_month = int(re_les_month)
    les_coms_dt = int(les_coms_dt)  
    
    with open("Resale_Flat_Prices_Model_1.pkl", "rb") as f:
        reg_model = pickle.load(f)

    user_data = np.array([[year, town, flat_type, flr_area_sqm, flat_model, stry_start, stry_end, re_les_year, re_les_month, les_coms_dt]])
    user_data = user_data.clip(min=0)
    y_pred = reg_model.predict(user_data)
    price = np.exp(y_pred[0])

    return round(price)

# Streamlit configuration
st.set_page_config(layout="wide")
st.title(":red[Singapore Resale Flat Prices Prediction]")

# Sidebar menu
with st.sidebar:
    select = option_menu("MAIN MENU", ["Home", "Price Prediction", "About"])

# Home section
if select == "Home":
    st.header(":orange[HDB Flats]")
    st.write("The majority of Singaporeans live in public housing provided by the Housing and Development Board. HDB flats can be purchased either directly from the HDB as a new unit or through the resale market from existing owners.")
    st.header(":orange[Resale Process]")
    st.write("In the resale market, buyers purchase flats from existing flat owners, and the transactions are facilitated through the HDB resale process. The process involves a series of steps, including valuation, negotiations, and the submission of necessary documents.")
    st.header(":orange[Valuation]")
    st.write("The HDB conducts a valuation of the flat to determine its market value. This is important for both buyers and sellers in negotiating a fair price.")
    st.header(":orange[HDB Loan and Bank Loan]")
    st.write("Buyers can choose to finance their flat purchase through an HDB loan or a bank loan. HDB loans are provided by the HDB, while bank loans are obtained from commercial banks.")
    st.header(":orange[Market Trends]")
    st.write("The resale market is influenced by various factors such as economic conditions, interest rates, and government policies. Property prices in Singapore can fluctuate based on these factors.")
    st.header(":orange[Online Platforms]")
    st.write("There are online platforms and portals where sellers can list their resale flats, and buyers can browse available options.")

# Price Prediction section
elif select == "Price Prediction":
    st.header("Predict Resale Flat Prices")
    st.write(":orange[Enter the details below to get the predicted resale price of an HDB flat.]")

    col1, col2 = st.columns(2)
    with col1:
        year = st.selectbox("Select the Year", [str(i) for i in range(2015, 2025)], help="Year of the resale transaction.")
        town = st.selectbox("Select the Town", ['ANG MO KIO', 'BEDOK', 'BISHAN', 'BUKIT BATOK', 'BUKIT MERAH',
                                                'BUKIT PANJANG', 'BUKIT TIMAH', 'CENTRAL AREA', 'CHOA CHU KANG',
                                                'CLEMENTI', 'GEYLANG', 'HOUGANG', 'JURONG EAST', 'JURONG WEST',
                                                'KALLANG/WHAMPOA', 'MARINE PARADE', 'PASIR RIS', 'PUNGGOL',
                                                'QUEENSTOWN', 'SEMBAWANG', 'SENGKANG', 'SERANGOON', 'TAMPINES',
                                                'TOA PAYOH', 'WOODLANDS', 'YISHUN'], help="Town where the flat is located.")
        flat_type = st.selectbox("Select the Flat Type", ['1 ROOM', '2 ROOM', '3 ROOM', '4 ROOM', '5 ROOM', 'EXECUTIVE', 'MULTI-GENERATION'], help="Type of the flat.")
        flr_area_sqm = st.number_input(f"Enter the Floor Area (sqm) (Min: {MIN_FLOOR_AREA} / Max: {MAX_FLOOR_AREA})", min_value=MIN_FLOOR_AREA, max_value=MAX_FLOOR_AREA, help="Floor area of the flat in square meters.")
        flat_model = st.selectbox("Select the Flat Model", ['2-room', '3Gen', 'Adjoined flat', 'Apartment', 'DBSS', 'Improved', 'Improved-Maisonette', 'Maisonette', 'Model A', 'Model A-Maisonette', 'Model A2', 'Multi Generation', 'New Generation', 'Premium Apartment', 'Premium Apartment Loft', 'Premium Maisonette', 'Simplified', 'Standard', 'Terrace', 'Type S1', 'Type S2'], help="Model of the flat.")

    with col2:
        stry_start = st.number_input(f"Enter the Storey Start (Min: {MIN_STOREY_START})", min_value=MIN_STOREY_START, max_value=MAX_STOREY_END, help="Starting storey of the flat.")
        stry_end = st.number_input(f"Enter the Storey End (Min: {stry_start})", min_value=stry_start, max_value=MAX_STOREY_END, help="Ending storey of the flat.")
        re_les_year = st.number_input(f"Enter the Remaining Lease Year (Min: {MIN_REMAINING_LEASE_YEAR} / Max: {MAX_REMAINING_LEASE_YEAR})", min_value=MIN_REMAINING_LEASE_YEAR, max_value=MAX_REMAINING_LEASE_YEAR, help="Remaining lease years of the flat.")
        re_les_month = st.number_input(f"Enter the Remaining Lease Month (Min: {MIN_REMAINING_LEASE_MONTH} / Max: {MAX_REMAINING_LEASE_MONTH})", min_value=MIN_REMAINING_LEASE_MONTH, max_value=MAX_REMAINING_LEASE_MONTH, help="Remaining lease months of the flat.")
        les_coms_dt = st.selectbox("Select the Lease Commence Date", [str(i) for i in range(1966, 2023)], help="Year the lease commenced.")

    button = st.button("Predict the Price")

    if button:
        pre_price = predict_price(year, town, flat_type, flr_area_sqm, flat_model, stry_start, stry_end, re_les_year, re_les_month, les_coms_dt)
        if pre_price:
            st.write(f"## :green[*The Predicted Price is:*] ${pre_price}")
        else:
            st.write(f"## :red[*Prediction could not be made due to invalid inputs. Please check and try again.*]")

# About section
elif select == "About":
    st.header("About This App")
    st.write("This application predicts the resale prices of HDB flats in Singapore using a pre-trained machine learning model. Enter the required details in the 'Price Prediction' section to get the predicted price of a resale flat.")
    st.header("About Me")
    Name = (f'{"Name :"}  {"KESHAV KUMAR"}')
    mail = (f'{"Mail :"}  {"keshavkumar.1023@gmail.com"}')
    social_media = {
        "GITHUB": "https://github.com/keshavk1023",
        "LINKEDIN": "www.linkedin.com/in/keshav-kumar-8075a5185"}

    st.subheader(Name)
    st.subheader(mail)

    st.write("#")
    cols = st.columns(len(social_media))
    for index, (platform, link) in enumerate(social_media.items()):
        cols[index].write(f"[{platform}]({link})")    