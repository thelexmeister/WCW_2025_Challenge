import pandas as pd
import streamlit as st
import requests
from io import StringIO

# GitHub Repository details
REPO_OWNER = 'thelexmeister'  # Replace with your GitHub username
REPO_NAME = 'WCW_2025_Challenge'     # Replace with your repository name
CSV_FILE = 'selected_teams.csv'               # The file where teams are stored
GITHUB_TOKEN = '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'   # Replace with your GitHub Personal Access Token

# Set up the GitHub API headers
headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3.raw',  # To fetch raw file content
}

# GitHub API URL for accessing the file in the repository
repo_url = f'https://api.github.com/{REPO_OWNER}/{REPO_NAME}/blob/main/{CSV_FILE}'
      
# Load data from an Excel file
df = pd.read_excel('WCW_2025 - players and prices.xlsx')

# Round the 'Price' column to whole numbers
df['Price'] = df['Price'].round(0).astype(int)

# App Header
st.header("Welcome to the 2025 WCW Challenge")
st.write("Use the table and the dropdowns to pick your team.")
st.write("You have $12,000. CLICK the save button at the end to save your team.")

# Add a position filter (selectbox to choose a position)
position_filter = st.selectbox("Select Position - use this dropdown to filter by position", ['All', 'QB', 'RB', 'WR', 'TE', 'K', 'DST'])

# Filter the dataframe based on selected position
if position_filter != 'All':
    filtered_df = df[df['Position'] == position_filter]
else:
    filtered_df = df

# Display the filtered dataframe (for debugging purposes)
st.write(filtered_df)

# Input field for team name
team_name = st.text_input("Enter your team name", "")

# Ensure team name is not empty before allowing to save
if not team_name:
    st.warning("Please enter a team name before saving.")

# Select players for each position
qb = st.selectbox("Select Quarterback", filtered_df[filtered_df['Position'] == 'QB']['Player'].tolist(), key="qb_select")
rb1 = st.selectbox("Select Running Back 1", filtered_df[filtered_df['Position'] == 'RB']['Player'].tolist(), key="rb1_select")
rb2 = st.selectbox("Select Running Back 2", filtered_df[filtered_df['Position'] == 'RB']['Player'].tolist(), key="rb2_select")
wr1 = st.selectbox("Select Wide Receiver 1", filtered_df[filtered_df['Position'] == 'WR']['Player'].tolist(), key="wr1_select")
wr2 = st.selectbox("Select Wide Receiver 2", filtered_df[filtered_df['Position'] == 'WR']['Player'].tolist(), key="wr2_select")
te = st.selectbox("Select Tight End", filtered_df[filtered_df['Position'] == 'TE']['Player'].tolist(), key="te_select")
k = st.selectbox("Select a Kicker", filtered_df[filtered_df['Position'] == 'K']['Player'].tolist(), key="k_select")
dst = st.selectbox("Select a Defense", filtered_df[filtered_df['Position'] == 'DST']['Player'].tolist(), key="dst_select")

# Select flex players (RB, WR, TE)
flex = st.multiselect("Select Flex Players", filtered_df[(filtered_df['Position'] == 'RB') | (filtered_df['Position'] == 'WR') | (filtered_df['Position'] == 'TE')]['Player'].tolist(), key="flex_select")

# Combine selected players into a list
selected_players = [qb, rb1, rb2, wr1, wr2, te, k, dst] + flex

# Display the selected players
st.write("Your selected players:", selected_players)

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
        st.write(f"{player}: ${price}")

# Save the selected team to GitHub (only if a team name is provided)
if st.button("Save Team") and team_name:
    try:
        # Fetch the existing CSV content from GitHub
        response = requests.get(repo_url, headers=headers)
        response.raise_for_status()

        # Decode and load the CSV content into a DataFrame
        file_content = response.json()['content']
        file_content = requests.utils.unquote(file_content)
        decoded_content = StringIO(file_content)
        teams_df = pd.read_csv(decoded_content)

    except requests.exceptions.RequestException as e:
        # If the file does not exist or cannot be fetched, create a new one
        teams_df = pd.DataFrame(columns=['Team Name', 'Players', 'Total Price'])
    
    # Add new team to the DataFrame using pd.concat (instead of append)
    new_team = pd.DataFrame({'Team Name': [team_name], 'Players': [', '.join(selected_players)], 'Total Price': [total_price]})
    teams_df = pd.concat([teams_df, new_team], ignore_index=True)

    # Convert DataFrame to CSV format and upload it back to GitHub
    csv_data = teams_df.to_csv(index=False)

    # Prepare the data to update the file
    update_url =  f'https://api.github.com/{REPO_OWNER}/{REPO_NAME}/blob/main/{CSV_FILE}'
    data = {
        'message': f"Added team '{team_name}' with total price {total_price}",
        'content': requests.utils.quote(csv_data),  # base64 encode the CSV
        'sha': response.json()['sha'] if 'sha' in response.json() else '',  # To ensure the correct file version
    }

    # Update the file via the GitHub API
    update_response = requests.put(update_url, json=data, headers=headers)
    update_response.raise_for_status()

    st.success(f"Your team '{team_name}' has been saved to GitHub!")
