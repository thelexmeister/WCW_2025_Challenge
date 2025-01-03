import streamlit as st
import pandas as pd

# Example dataframe (replace with actual data)
data = {
    'Player': ['Player A', 'Player B', 'Player C', 'Player D', 'Player E', 'Player F', 'Player G', 'Player H'],
    'Position': ['QB', 'RB', 'RB', 'WR', 'WR', 'TE', 'RB', 'WR']
}

df = pd.DataFrame(data)

# App Header
st.header("Your Fantasy Team")

# Select players for each position
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

# Show selected players
st.write("Your selected players:", selected_players)

# Save selected team (optional)
if st.button("Save Team"):
    # Example: Save to a CSV or append to an existing list
    team_data = {'Player': selected_players}
    team_df = pd.DataFrame(team_data)
    team_df.to_csv(f"{qb}_team.csv", index=False)  # Saves the team to a CSV file based on QB's name
    st.success("Your team has been saved!")
