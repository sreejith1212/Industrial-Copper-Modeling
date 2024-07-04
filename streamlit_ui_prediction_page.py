import streamlit as st
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_option_menu import option_menu



def status_predict(quantity_tons, customer, country, item_type, application, thickness, width, product_ref, selling_price, 
                   item_day, item_month, item_year, delivery_day, delivery_month, delivery_year):

    with open("E:\GUVI Main Boot\project copper modelling\Industrial-Copper-Modeling\status_prediction_model.pkl", "rb") as file:
        status_prediction_model = pickle.load(file)

    
    with open("E:\GUVI Main Boot\project copper modelling\Industrial-Copper-Modeling\label_encoder_item_type.pkl", "rb") as file:
        label_encoder_item = pickle.load(file)

    encoded_item_type = label_encoder_item.transform([item_type])[0]

    data = np.array([[quantity_tons, customer, country, encoded_item_type, application, thickness, width, product_ref, 
                      selling_price, item_day, item_month, item_year, delivery_day, delivery_month, delivery_year]])

    input_predict_status = status_prediction_model.predict(data)

    return input_predict_status

    
def selling_price_predict(quantity_tons, customer, country, item_type, application, thickness, width, product_ref, status, 
                          item_day, item_month, item_year, delivery_day, delivery_month, delivery_year):

    with open("E:\GUVI Main Boot\project copper modelling\Industrial-Copper-Modeling\selling_price_prediction_model.pkl", "rb") as file:
        selling_price_prediction_model = pickle.load(file)

    with open("E:\GUVI Main Boot\project copper modelling\Industrial-Copper-Modeling\label_encoder_item_type.pkl", "rb") as file:
        label_encoder_item = pickle.load(file)

    encoded_item_type = label_encoder_item.transform([item_type])[0]

    if status == "Won":
        status = 1
    elif status == "Lost":
        status = 0
    else:
        status = 2

    data = np.array([[quantity_tons, customer, country, status, encoded_item_type, application, thickness, width, product_ref, 
                       item_day, item_month, item_year, delivery_day, delivery_month, delivery_year]])

    input_predict_selling_price = selling_price_prediction_model.predict(data)
    input_predict_selling_price = np.exp(input_predict_selling_price)

    return input_predict_selling_price

if __name__ == "__main__":

    # set app page layout type
    st.set_page_config(layout="wide")

    # create sidebar
    with st.sidebar:        
        page = option_menu(
                            menu_title='Copper Modelling',
                            options=['Home','Predict Order Status', 'Predict Selling Price'],
                            icons=['gear', 'map', 'bar-chart-line'],
                            menu_icon="pin-map-fill",
                            default_index=0 ,
                            styles={"container": {"padding": "5!important"},
                                    "icon": {"color": "brown", "font-size": "23px"}, 
                                    "nav-link": {"color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "lightblue", "display": "flex", 
                                                 "align-items": "center"},
                                    "nav-link-selected": {"background-color": "grey"},}  
        )


if page == "Home":

    st.header("Industrial Copper Modeling", divider = "rainbow")
    st.write("")

    st.subheader(":orange[Application Properties :]")
    st.subheader(":one: :grey[_Lead Status Prediction Using Classification Model_.]")
    st.subheader(":two: :grey[_Selling Price Prediction Using Regression Model_.]")

if page == "Predict Order Status":

    col1, col2, col3 = st.columns([1,2,1])
    col2.header(':green[Predict Customer Order Status] 🏭')
    container_upload = st.container(height=600, border=False)
    for i in range(3):
        container_upload.write("")
    with container_upload.form(key = "stat"):
        col14, col15, col16 = st.columns(3)
        quantity_tons = col14. number_input(label="Quantity In Tons 🏟️")
        customer = col15.number_input(label="Customer ID 👨‍🏭", value=0)
        country = col16.number_input(label="Country 🌐", value=0)
        item_type = col14.text_input(label="Item Type 📧")
        application = col14.number_input(label="Application 📱", value=0)
        thickness = col15.number_input(label="Thickness 🌆")
        width = col16.number_input(label="Width 🌃")
        product_ref = col15.number_input(label="Product Reference 🌇", value=0)
        selling_price = col16.number_input(label="Selling Price 💼")
        item_day = col14.selectbox(label="Item Day 📋", options=tuple(range(1, 32)))
        item_month = col15.selectbox(label="Item Month 💾", options=tuple(range(1, 13)))
        item_year = col16.selectbox(label="Item Year 📆", options=tuple(range(2020, 2028)))
        delivery_day = col14.selectbox(label="Delivery Day 📋", options=tuple(range(1, 32)))
        delivery_month = col15.selectbox(label="Delivery Month 💾", options=tuple(range(1, 13)))
        delivery_year = col16.selectbox(label="Delivery Year 📆", options=tuple(range(2020, 2028)))

        upload_data = col16.form_submit_button(label="Predict Status", help="Click to Predict Order Status!", type = "primary")
    
    col4, col5, col6 = st.columns(3)
    if upload_data:
        try:
            prediction_1 = status_predict(np.log(quantity_tons), customer, country, item_type, application, np.log(thickness), width, product_ref, np.log(selling_price), 
                                        item_day, item_month, item_year, delivery_day, delivery_month, delivery_year)

            if prediction_1 == 1:
                col4.success(f"Predicted Order Status is : Won 🎊")
            else:
                col4.error(f"Predicted Order Status is: Lost 🚨")
        except:
            col4.error("Enter valid values 🚨")
            
if page == "Predict Selling Price":

    col1, col2, col3 = st.columns([1,2,1])
    col2.header(':green[Predict Item Selling Price] 🏭')
    container_upload = st.container(height=600, border=False)
    for i in range(3):
        container_upload.write("")
    with container_upload.form(key = "sell"):
        col14, col15, col16 = st.columns(3)
        quantity_tons = col14. number_input(label="Quantity In Tons 🏟️")
        customer = col15.number_input(label="Customer ID 👨‍🏭", value=0)
        country = col16.number_input(label="Country 🌐", value=0)
        item_type = col14.text_input(label="Item Type 📧")
        application = col14.number_input(label="Application 📱", value=0)
        thickness = col15.number_input(label="Thickness 🌆")
        width = col16.number_input(label="Width 🌃")
        product_ref = col15.number_input(label="Product Reference 🌇", value=0)
        status = col16.selectbox(label="Order Status 💼", options=['Won', 'Draft', 'To be approved', 'Lost', 'Not lost for AM','Wonderful', 'Revised', 'Offered', 'Offerable'])
        item_day = col14.selectbox(label="Item Day 📋", options=tuple(range(1, 32)))
        item_month = col15.selectbox(label="Item Month 💾", options=tuple(range(1, 13)))
        item_year = col16.selectbox(label="Item Year 📆", options=tuple(range(2020, 2028)))
        delivery_day = col14.selectbox(label="Delivery Day 📋", options=tuple(range(1, 32)))
        delivery_month = col15.selectbox(label="Delivery Month 💾", options=tuple(range(1, 13)))
        delivery_year = col16.selectbox(label="Delivery Year 📆", options=tuple(range(2020, 2028)))

        upload_data = col16.form_submit_button(label="Predict Selling Price", help="Click to Predict Item Selling Price!", type = "primary")
    
    col4, col5, col6 = st.columns(3)
    if upload_data:
        try:
            prediction_1 = selling_price_predict(np.log(quantity_tons), customer, country, item_type, application, np.log(thickness), width, product_ref, status, 
                                        item_day, item_month, item_year, delivery_day, delivery_month, delivery_year)
            
            col4.success(f"Predicted Item Selling Price : $ {round(prediction_1[0])} 💰")
        except:
            col4.error("Enter valid values 🚨")

            