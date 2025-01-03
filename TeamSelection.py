import streamlit as st
import pandas as pd

# Load data from an Excel file
# Make sure the Excel file is placed in the same directory as your script or provide the full path to the file
df = pd.read_excel('players.xlsx')

# Display the dataframe (for debugging purposes, you can remove this line later)
st.write(df)

# App Header
st.header("Your Fantasy Team")

# Select players for each position (filter players by position)
qb = st.selectbox("Select Quarterback", df[df['Position'] == 'QB']['Player'].tolist(), key="qb_select")
rb1 = st.selectbox("Select Running Back 1", df[df['Position'] == 'RB']['Player'].tolist(), key="rb1_select")
rb2 = st.selectbox("Select Running Back 2", df[df['Position'] == 'RB']['Player'].tolist(), key="rb2_select")
wr1 = st.selectbox("Select Wide Receiver 1", df[df['Position'] == 'WR']['Player'].tolist(), key="wr1_select")
wr2 = st.selectbox("Select Wide Receiver 2", df[df['Position'] == 'WR']['Player'].tolist(), key="wr2_select")
te = st.selectbox("Select Tight End", df[df['Position'] == 'TE']['Player'].tolist(), key="te_select")

# Select flex players (RB, WR, TE)
flex = st.multiselect("Select Flex Players", df[(df['Position'] == 'RB') | (df['Position'] == 'WR') | (df['Position'] == 'TE')]['Player'].tolist(), max_selections=2, key="flex_select")

# Combine selected players into a list
selected_players = [qb, rb1, rb2, wr1, wr2, te] + flex

# Display the selected players
st.write("Your selected players:", selected_players)

# Display the price of the selected players
total_price = 0
for player in selected_players:
    price = df[df['Player'] == player]['Price'].values[0]
    total_price += price
    st.write(f"{player}: ${price}")

st.write(f"Total Price: ${total_price}")

# Save the selected team (optional)
if st.button("Save Team"):
    # Example: Save to a CSV or append to an existing list
    team_data = {'Player': selected_players}
    team_df = pd.DataFrame(team_data)
    team_df['Total Price'] = total_price
    team_df.to_csv(f"{qb}_team.csv", index=False)  # Saves the team to a CSV file based on QB's name
    st.success("Your team has been saved!")

