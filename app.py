import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Database connection details using SQLAlchemy
connection_string = (
    "mssql+pyodbc://admin-owner:carlito99!!@carlitodatabase.database.windows.net:1433/DataStorage?"
    "driver=ODBC+Driver+17+for+SQL+Server"
)

# Function to fetch data from the database -- returns a DataFrame
def fetch_data():
    try:
        engine = create_engine(connection_string)
        query = "SELECT * FROM mqtt_processed_data"
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
        return pd.DataFrame()

# Streamlit app
st.title("MQTT Processed Data Dashboard")

# Fetch and display data
data = fetch_data()

if not data.empty:
    # Display the raw data in a table
    st.write("### MQTT Processed Data")
    st.dataframe(data)

    # Display charts or statistics
    st.write("### Data Statistics")
    st.write(data.describe())

    # Example: Plot a histogram for a numeric column (if available)
    numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns
    if len(numeric_columns) > 0:
        selected_column = st.selectbox("Select a column to plot", numeric_columns)
        st.write(f"### Histogram for {selected_column}")
        st.bar_chart(data[selected_column])
else:
    st.warning("No data found in the database.") 