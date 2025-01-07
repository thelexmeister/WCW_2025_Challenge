import pandas as pd
import streamlit as st

# Load data from an Excel file
df = pd.read_excel('WCW_2025 - players and prices.xlsx')

# Round the 'Price' column to whole numbers
df['Price'] = df['Price'].round(0).astype(int)

# App Header
st.header("Welcome to the 2025 WCW Challenge")
st.markdown(" ")
st.write("Use the table below, which has all the prices for the available players, and the dropdown to filter the table by position. Use the dropdowns on the right side to pick your players.")
st.write("The players you choose will show on the sidebar (left) so you can see the total cost of your team.")
st.write("PICK: 1 QB, 2 RB, 2 WR, 1 TE, 2 FLEX, 1 K and 1 DST")
st.write("You have $12,000. Once you have settled on your team, send me a screenshot of your team and team name, from the sidebar, via text. If you can't see the sidebar, use the little > in the upper left corner to unhide the sidebar.")
# Input field for team name
team_name = st.text_input("Enter your team name", "")


# Create two columns for layout
col1, col2 = st.columns(2)

# Left Column - Your Team
with col1:
    # Add a position filter (selectbox to choose a position)
    position_filter = st.multiselect("Select Position - use this dropdown to filter by position", ['All', 'QB', 'RB', 'WR', 'TE', 'K', 'DST'])
    
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
    qb  = st.selectbox("Select Quarterback",     df[df['Position'] == 'QB']['Player'].tolist(), key="qb_select")
    rb1 = st.selectbox("Select Running Back 1",  df[df['Position'] == 'RB']['Player'].tolist(), key="rb1_select")
    rb2 = st.selectbox("Select Running Back 2",  df[df['Position'] == 'RB']['Player'].tolist(), key="rb2_select")
    wr1 = st.selectbox("Select Wide Receiver 1", df[df['Position'] == 'WR']['Player'].tolist(), key="wr1_select")
    wr2 = st.selectbox("Select Wide Receiver 2", df[df['Position'] == 'WR']['Player'].tolist(), key="wr2_select")
    te  = st.selectbox("Select Tight End",       df[df['Position'] == 'TE']['Player'].tolist(), key="te_select")
    
    # Select flex players (RB, WR, TE)
    flex1 = st.multiselect("Select Flex Player 1", df[(df['Position'] == 'RB') | (df['Position'] == 'WR') | (df['Position'] == 'TE')]['Player'].tolist(), key="flex1_select")
    flex2 = st.multiselect("Select Flex Player 2", df[(df['Position'] == 'RB') | (df['Position'] == 'WR') | (df['Position'] == 'TE')]['Player'].tolist(), key="flex2_select")
    
    k   = st.selectbox("Select a Kicker", df[df['Position'] == 'K']['Player'].tolist(), key="k_select")
    dst = st.selectbox("Select a Defense", df[df['Position'] == 'DST']['Player'].tolist(), key="dst_select")
    
    # Combine selected players into a list
    selected_players = [qb, rb1, rb2, wr1, wr2, te] + flex1 + flex2 + [k, dst]

# Sidebar styling using CSS to make sure the sidebar is visible and fixed
st.markdown("""
    <style>
        /* Make sidebar fixed and always open */
        .css-1d391kg {  /* Adjust this class name as per your Streamlit version */
            position: fixed !important;
            left: 0 !important;
            top: 0 !important;
            height: 100vh !important;
            width: 250px !important; /* Set width of sidebar */
        }
        
        /* Adjust content's margin to account for sidebar */
        .css-1outpf7 {  
            margin-left: 250px !important;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar content
with st.sidebar:
    st.write("Your selected players:")
    st.write("Don't forget to take a picture")
    st.write(" ")
    
    # Team Name display with custom styling
    st.write(f"<span style='color:red; font-size:16px; display:inline;'>Team Name: </span><span style='font-size:16px; display:inline;'>{team_name}</span>", unsafe_allow_html=True)
    
    # Calculate and display the price of the selected players
    total_price = 0
    for player in selected_players:
        player_row = df[df['Player']   == player]
                
        # Ensure player exists in the filtered data
        if player_row.empty:
            st.sidebar.warning(f"Player '{player}' not found in the filtered list.")
        else:
            price = player_row['Price'].values[0]
            position = player_row['Position'].values[0]
            total_price += price
            # Display each player's price in the sidebar
            st.sidebar.write(f"<span style='color:blue; font-size:16px; display:inline;'>{player}({position}): </span><span style='font-size:16px; display:inline;'>${price}</span>", unsafe_allow_html=True)

if total_price > 12000:
    st.sidebar.markdown(f"<h3 style='color:red;'>Total Price: ${total_price}</h3>", unsafe_allow_html=True)
else:
    st.sidebar.markdown(f"<h3 style='color:green;'>Total Price: ${total_price}</h3>", unsafe_allow_html=True)
            




