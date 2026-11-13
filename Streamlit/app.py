import streamlit as st

st.set_page_config(
    page_title="OLA Ride Insights",
    page_icon="🚗",
    layout="wide"
)

st.title("OLA Ride Insights Dashboard")
st.subheader("Explore booking, revenue, vehicle and customer insights")

import pandas as pd

# Load the cleaned OLA dataset
df = pd.read_csv("Dataset/ola_cleaned.csv")

st.success("Dataset loaded successfully!")

st.write("### OLA Ride Dataset")
st.write("Total Records:", len(df))

st.dataframe(df.head(10))

# Key Performance Indicators

total_rides = len(df)

successful_rides = df[
    df["Booking_Status"] == "Success"
].shape[0]

total_revenue = df.loc[
    df["Booking_Status"] == "Success",
    "Booking_Value"
].sum()

average_distance = df.loc[
    df["Booking_Status"] == "Success",
    "Ride_Distance"
].mean()

st.write("## Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Rides", f"{total_rides:,}")
col2.metric("Successful Rides", f"{successful_rides:,}")
col3.metric("Total Revenue", f"₹{total_revenue:,.0f}")
col4.metric("Average Ride Distance", f"{average_distance:.2f} km")

# Booking Status Distribution

st.write("## Booking Status Distribution")

status_count = df["Booking_Status"].value_counts()

st.bar_chart(status_count)

# Ride Distance by Vehicle Type

st.write("## Average Ride Distance by Vehicle Type")

vehicle_distance = df[
    df["Booking_Status"] == "Success"
].groupby("Vehicle_Type")["Ride_Distance"].mean()

st.bar_chart(vehicle_distance)

# Revenue by Payment Method

st.write("## Revenue by Payment Method")

successful_df = df[df["Booking_Status"] == "Success"]

payment_revenue = successful_df.groupby(
    "Payment_Method"
)["Booking_Value"].sum()

st.bar_chart(payment_revenue)

# Customer Cancellation Reasons

st.write("## Customer Cancellation Reasons")

customer_cancel = df[
    "Canceled_Rides_by_Customer"
].dropna().value_counts()

st.bar_chart(customer_cancel)

# Driver Cancellation Reasons

st.write("## Driver Cancellation Reasons")

driver_cancel = df[
    "Canceled_Rides_by_Driver"
].dropna().value_counts()

st.bar_chart(driver_cancel)

# Driver Ratings Distribution

st.write("## Driver Ratings Distribution")

driver_ratings = df["Driver_Ratings"].dropna()

st.bar_chart(driver_ratings.value_counts().sort_index())

# Customer Ratings Distribution

st.write("## Customer Ratings Distribution")

customer_ratings = df["Customer_Rating"].dropna()

st.bar_chart(customer_ratings.value_counts().sort_index())

# Customer vs Driver Ratings

st.write("## Customer vs Driver Ratings")

ratings_df = df[
    ["Customer_Rating", "Driver_Ratings"]
].dropna()

st.scatter_chart(
    ratings_df,
    x="Customer_Rating",
    y="Driver_Ratings"
)