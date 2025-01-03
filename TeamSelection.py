import streamlit as st
import pandas as pd

# Load data from an Excel file
df = pd.read_excel('WCW_2025 - players and prices.xlsx')

# App Header
st.header("Welcome to the 2025 WCW Challenge")
st.write("Use the table and the dropdowns to pick your team.")
st.write("You have $12,000. CLICK the save button at the end to save your team.")

# Add a position filter (selectbox to choose a position)
position_filter = st.selectbox("Select Position - use this dropdown to filter by position", ['All', 'QB', 'RB', 'WR', 'TE'])

# Filter the dataframe based on selected position
if position_filter != 'All':
    filtered_df = df[df['Position'] == position_filter]
else:
    filtered_df = df

# Display the filtered dataframe (for debugging purposes)
st.write(filtered_df)

# Select players for each position
qb = st.selectbox("Select Quarterback", filtered_df[filtered_df['Position'] == 'QB']['Player'].tolist(), key="qb_select")
rb1 = st.selectbox("Select Running Back 1", filtered_df[filtered_df['Position'] == 'RB']['Player'].tolist(), key="rb1_select")
rb2 = st.selectbox("Select Running Back 2", filtered_df[filtered_df['Position'] == 'RB']['Player'].tolist(), key="rb2_select")
wr1 = st.selectbox("Select Wide Receiver 1", filtered_df[filtered_df['Position'] == 'WR']['Player'].tolist(), key="wr1_select")
wr2 = st.selectbox("Select Wide Receiver 2", filtered_df[filtered_df['Position'] == 'WR']['Player'].tolist(), key="wr2_select")
te = st.selectbox("Select Tight End", filtered_df[filtered_df['Position'] == 'TE']['Player'].tolist(), key="te_select")

# Select flex players (RB, WR, TE)
flex = st.multiselect("Select Flex Players", filtered_df[(filtered_df['Position'] == 'RB') | (filtered_df['Position'] == 'WR') | (filtered_df['Position'] == 'TE')]['Player'].tolist(), max_selections=2, key="flex_select")

# Combine selected players into a list
selected_players = [qb, rb1, rb2, wr1, wr2, te] + flex

# Display the selected players
st.write("Your selected players:", selected_players)

# Calculate and display the price of the selected players
total_price = 0
for player in selected_players:
    price = filtered_df[filtered_df['Player'] == player]['Price'].values[0]
    
    # Ensure the price is a whole number
    price = round(price)  # Option 1: Round the price to the nearest whole number
    # Alternatively, use: price = int(price)  # Option 2: Convert to integer (drops decimals)
    
    total_price += price
    st.write(f"{player}: ${price}")

# Display the total price with conditional coloring
if total_price <= 12000:
    st.markdown(f"<h3 style='color:green;'>Total Price: ${total_price}</h3>", unsafe_allow_html=True)
else:
    st.markdown(f"<h3 style='color:red;'>Total Price: ${total_price}</h3>", unsafe_allow_html=True)

# Save the selected team (optional)
if st.button("Save Team"):
    # Example: Save to a CSV or append to an existing list
    team_data = {'Player': selected_players}
    team_df = pd.DataFrame(team_data)
    team_df['Total Price'] = total_price
    team_df.to_csv(f"{qb}_team.csv", index=False)  # Saves the team to a CSV file based on QB's name
    st.success("Your team has been saved!")


