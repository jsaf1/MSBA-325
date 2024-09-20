import pandas as pd
import streamlit as st
import re
import plotly.express as px

# Load the CSV file (ensure the path is correct)
df = pd.read_csv("electricity.csv")

# Rename columns for clarity
df.rename(columns={
    'Type of alternative energy used - hydropower (water use)': 'Hydropower',
    'State of the lighting network - bad': 'Lighting_Bad',
    'State of the lighting network - acceptable': 'Lighting_Acceptable',
    'State of the lighting network - good': 'Lighting_Good',
    'State of the power grid - good': 'Grid_Good',
    'State of the power grid - acceptable': 'Grid_Acceptable',
    'State of the power grid - bad': 'Grid_Bad',
    'Existence of alternative energy - exists': 'AltEnergy_Exists',
    'Existence of alternative energy - does not exist': 'AltEnergy_NotExists',
    'Type of alternative energy used - solar energy': 'SolarEnergy',
    'Type of alternative energy used - wind energy': 'WindEnergy',
    'Type of alternative energy used - other': 'OtherEnergy',
    'refArea': 'Region',
    'Town': 'Town'
}, inplace=True)

# Convert alternative energy existence columns into a single Boolean or categorical column
df['AltEnergy_Status'] = df['AltEnergy_Exists'].apply(lambda x: 'Exists' if x == 1 else 'Not Exists')

# Drop the original redundant columns
df.drop(columns=['AltEnergy_Exists', 'AltEnergy_NotExists'], inplace=True)

# Preprocessing to extract region names from the URLs in the 'refArea' column
df['Region'] = df['Region'].apply(lambda x: re.split(r'[/#]', x)[-1].replace('_', ' '))

# Display the unique regions to verify (in Streamlit)
st.write("<b>List of the regions in Lebanon:</b>", unsafe_allow_html=True)
st.write(df['Region'].unique())




# Sidebar dropdown to select energy types for the first chart
energy_type = st.sidebar.multiselect(
    'Select energy types for the first chart',
    ['Hydropower', 'SolarEnergy', 'WindEnergy', 'OtherEnergy'],
       default=['Hydropower', 'SolarEnergy', 'WindEnergy', 'OtherEnergy']  # All energy types selected by default
)


# Summing the total of selected energy types across all regions for the pie chart
total_energy = df[energy_type].sum().reset_index()
total_energy.columns = ['Energy Type', 'Total']

# Create the pie chart
fig1 = px.pie(total_energy, 
                 names='Energy Type', 
                 values='Total', 
                 title='Overall Proportion of Selected Energy Types')

# Display the pie chart
st.plotly_chart(fig1)




# Group data by region and sum the values of each energy type
energy_by_region = df.groupby('Region')[['Hydropower', 'SolarEnergy', 'WindEnergy', 'OtherEnergy']].sum().reset_index()


# Filter data for the first chart
filtered_data = energy_by_region[['Region'] + energy_type]

# Create the first figure
fig2 = px.bar(filtered_data,
              x='Region',
              y=energy_type,
              title='Distribution of Selected Energy Types by Region',
              labels={'value': 'Number of Towns', 'Region': 'Region', 'variable': 'Energy Type'},
              barmode='stack')

# Display the first figure
st.plotly_chart(fig2)



