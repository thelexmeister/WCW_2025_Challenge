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


# Create two columns for layout
col1, col2 = st.columns(2)

# Left Column - Your Team
with col1:
    # Add a position filter (selectbox to choose a position)
    position_filter = st.selectbox("Select Position - use this dropdown to filter by position", ['All', 'QB', 'RB', 'WR', 'TE', 'K', 'DST'])
    
    # Filter the dataframe based on selected position
    if position_filter != 'All':
        filtered_df = df[df['Position'] == position_filter]
    else:
        filtered_df = df
        
    # Display the filtered dataframe (for debugging purposes)
    #st.write(filtered_df)
    st.dataframe(filtered_df, height=600) 

with col2:
    # Select players for each position
    qb = st.selectbox("Select Quarterback", df[df['Position'] == 'QB']['Player'].tolist(), key="qb_select")
    rb1 = st.selectbox("Select Running Back 1", df[df['Position'] == 'RB']['Player'].tolist(), key="rb1_select")
    rb2 = st.selectbox("Select Running Back 2", df[df['Position'] == 'RB']['Player'].tolist(), key="rb2_select")
    wr1 = st.selectbox("Select Wide Receiver 1", df[df['Position'] == 'WR']['Player'].tolist(), key="wr1_select")
    wr2 = st.selectbox("Select Wide Receiver 2", df[df['Position'] == 'WR']['Player'].tolist(), key="wr2_select")
    te = st.selectbox("Select Tight End", df[df['Position'] == 'TE']['Player'].tolist(), key="te_select")
    
    # Select flex players (RB, WR, TE)
    flex = st.multiselect("Select Flex Players", df[df['Position'] == 'RB') | (filtered_df['Position'] == 'WR') | (filtered_df['Position'] == 'TE')]['Player'].tolist(), key="flex_select")
    
    k = st.selectbox("Select a Kicker", df[df['Position'] == 'K']['Player'].tolist(), key="k_select")
    dst = st.selectbox("Select a Defense", df[df['Position'] == 'DST']['Player'].tolist(), key="dst_select")
    
    # Combine selected players into a list
    selected_players = [qb, rb1, rb2, wr1, wr2, te] + flex + [k, dst]

# Display the selected players
st.sidebar.write("Your selected players:")
st.sidebar.write(" ")
#st.write("<h5 style='color:blue;'> Team Name:</h5> ", team_name, unsafe_allow_html=True)
st.sidebar.write(f"<span style='color:red; font-size:16px; display:inline;'>Team Name: </span><span style='font-size:16px; display:inline;'>{team_name}</span>", unsafe_allow_html=True)
# Calculate and display the price of the selected players
total_price = 0
for player in selected_players:
    # Filter to get the row for the selected player
    player_row = filtered_df[filtered_df['Player'] == player]

    # Check if the player exists in the filtered dataframe
    if player_row.empty:
        st.sidebar.warning(f"Player '{player}' not found in the filtered list.")
    else:
        # Retrieve the price if the player exists
        price = player_row['Price'].values[0]
        total_price += price
        st.sidebar.write(f"<span style='color:blue; font-size:16px; display:inline;'>{player}: </span><span style='font-size:16px; display:inline;'>${price}</span>", unsafe_allow_html=True)
# Display the total price with color based on condition
if total_price > 12000:
    st.sidebar.markdown(f"<h3 style='color:red;'>Total Price: ${total_price}</h3>", unsafe_allow_html=True)
else:
    st.sidebar.markdown(f"<h3 style='color:green;'>Total Price: ${total_price}</h3>", unsafe_allow_html=True)
