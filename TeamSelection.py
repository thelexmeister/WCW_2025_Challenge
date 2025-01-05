import pandas as pd
import streamlit as st

# Load data from an Excel file
df = pd.read_excel('WCW_2025 - players and prices.xlsx')

# Round the 'Price' column to whole numbers
df['Price'] = df['Price'].round(0).astype(int)

# App Header
st.header("Welcome to the 2025 WCW Challenge")
st.write("Use the table and the dropdowns to pick your team.")
st.write("You have $12,000. Once you have settled on your team, send me a screenshot of your team via text.")
# Input field for team name
team_name = st.text_input("Enter your team name", "")
# Add a position filter (selectbox to choose a position)
position_filter = st.selectbox("Select Position - use this dropdown to filter by position", ['All', 'QB', 'RB', 'WR', 'TE', 'K', 'DST'])

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
flex = st.multiselect("Select Flex Players", filtered_df[(filtered_df['Position'] == 'RB') | (filtered_df['Position'] == 'WR') | (filtered_df['Position'] == 'TE')]['Player'].tolist(), key="flex_select")

k = st.selectbox("Select a Kicker", filtered_df[filtered_df['Position'] == 'K']['Player'].tolist(), key="k_select")
dst = st.selectbox("Select a Defense", filtered_df[filtered_df['Position'] == 'DST']['Player'].tolist(), key="dst_select")

# Combine selected players into a list
selected_players = [qb, rb1, rb2, wr1, wr2, te] + flex + [k, dst]

# Display the selected players
st.write("Your selected players:")
st.write(" ")
st.write("Team Name: ", team_name)
# Calculate and display the price of the selected players
total_price = 0
for player in selected_players:
    # Filter to get the row for the selected player
    player_row = filtered_df[filtered_df['Player'] == player]

    # Check if the player exists in the filtered dataframe
    if player_row.empty:
        st.warning(f"Player '{player}' not found in the filtered list.")
    else:
        # Retrieve the price if the player exists
        price = player_row['Price'].values[0]
        total_price += price
        st.markdown(f"<h3 style='color:blue;'>Player: {player}: ${price}</h3>", unsafe_allow_html=True)

# Display the total price with color based on condition
if total_price > 12000:
    st.markdown(f"<h3 style='color:red;'>Total Price: ${total_price}</h3>", unsafe_allow_html=True)
else:
    st.markdown(f"<h3 style='color:green;'>Total Price: ${total_price}</h3>", unsafe_allow_html=True)
