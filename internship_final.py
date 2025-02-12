import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

# Set page configuration (must be at the very beginning)
st.set_page_config(layout="wide")
st.title('2025 Conference Carolinas Data Dashboard')
st.image("file.png")

# Cache the data to improve performance (use st.cache_data instead of st.cache)
@st.cache_data
def load_player_data():
    return pd.read_csv('2025 Conference Carolinas Player Stats.csv')

@st.cache_data
def load_team_data():
    return pd.read_csv('2025 Conference Carolinas Team Stats.csv')

# Load the player and team data
players_data = load_player_data()
team_data = load_team_data()

# Get unique teams from both player and team data
all_teams = list(set(players_data['Team'].unique()) | set(team_data['Team'].unique()))

# Sidebar for navigation
page = st.sidebar.radio("Select a page", ["Player Data", "Team Data"])

# Team Filter in the Sidebar (Global filter) - Multi-Select for Teams (works for both pages)
team_filter = st.sidebar.multiselect('Select Team(s) to Filter', ['All'] + all_teams, default=['All'])

# Apply filter globally to both players and team data
if 'All' not in team_filter:
    filtered_players_data = players_data[players_data['Team'].isin(team_filter)]
    filtered_team_data = team_data[team_data['Team'].isin(team_filter)]
else:
    filtered_players_data = players_data
    filtered_team_data = team_data

# Player Data Page
if page == "Player Data":
    st.header('Player Data Analysis')
    st.markdown("**Statistics for all Conference Carolinas players for the 2025 Men's Volleyball Season.**")

    # Create tabs for Scatter Plot and Bar Chart
    tab1, tab2, tab3 = st.tabs(['Scatter Plot', 'Bar Chart','Rotational Analysis'])

    # Scatter Plot Tab
    with tab1:
        st.subheader("Scatter Plot Controls")

        # Sidebar-like controls moved to the main area for this tab
        # Filter the players list based on the selected team(s)
        player = st.multiselect('Select players to compare', filtered_players_data['Name'])

        # Select the x and y axis
        x_val = st.selectbox("Pick your x-axis", filtered_players_data.select_dtypes(include=np.number).columns.tolist())
        y_val = st.selectbox("Pick your y-axis", filtered_players_data.select_dtypes(include=np.number).columns.tolist())

        # Check if x_val and y_val are different
        if x_val == y_val:
            st.warning("Please select different attributes for the x and y axes.")
        else:
            # Use a separate filtered dataset for the scatter plot
            scatter_data = filtered_players_data
            if player:
                scatter_data = scatter_data[scatter_data['Name'].isin(player)]
                st.dataframe(scatter_data)

            # Plot the scatter plot
            scatter = alt.Chart(scatter_data, title=f"{x_val} vs {y_val}").mark_point().encode(
                alt.X(x_val, title=f'{x_val}'),
                alt.Y(y_val, title=f'{y_val}'),
                color='Name',  # 'Name' can be used for categorical color encoding
                tooltip=['Name', 'Team', 'Position', x_val, y_val]
            ).configure_mark(
                opacity=0.7
            )

            st.altair_chart(scatter, theme="streamlit", use_container_width=True)

    # Bar Chart Tab
    with tab2:
        st.subheader("Bar Chart Controls")

        # Select attribute for the bar chart
        z_val = st.selectbox("Pick your attribute", filtered_players_data.select_dtypes(include=np.number).columns.tolist())
        count_input = st.number_input(f"Enter a value for the number of top {z_val} values to display", min_value=1, max_value=len(filtered_players_data), value=5, step=1)

        # Filter dataset based on the top values (no player filtering)
        top_data = filtered_players_data.nlargest(count_input, z_val)
        bar = alt.Chart(top_data).mark_bar().encode(
            y=alt.Y('Name', title='Name', sort='-x'),
            x=alt.X(z_val, title=f'{z_val}'),
            tooltip=['Name', 'Team', 'Position', z_val]
        ).properties(
            title=f"Top {count_input} Players by {z_val}"
        ).configure_mark(
            opacity=0.7
        )

        st.altair_chart(bar, use_container_width=True)
        
    with tab3:  # Third tab for Rotational Analysis
        st.subheader("Rotational Analysis")

    # Add content for rotational analysis here.
        st.markdown("**Analysis of player attack attempts and hitting percentage by rotation.**")

        rotation_columns = [col for col in filtered_players_data.columns if any(rot in col for rot in ['R1', 'R2', 'R3', 'R4', 'R5', 'R6'])]

    # Assuming the data contains fields for rotation analysis such as 'Attack Attempts' and 'Hitting Percentage'
        x_val = st.selectbox("Pick your x-axis", rotation_columns,key="x_axis_rotation")
        y_val = st.selectbox("Pick your y-axis", rotation_columns,key="y_axis_rotation")

    # Ensure x_val and y_val are different
        if x_val == y_val:
            st.warning("Please select different attributes for the x and y axes.")
        else:
        # Create the scatter plot using the selected axes
            scatter_data = filtered_players_data  # Use filtered player data for the scatter plot
            scatter = alt.Chart(scatter_data, title=f"{x_val} vs {y_val} by Rotation").mark_point().encode(
                alt.X(x_val, title=f'{x_val}'),
                alt.Y(y_val, title=f'{y_val}'),
                color='Name',  # Coloring by player name or any other relevant category
                tooltip=['Name', 'Team', 'Position', x_val, y_val]
            ).configure_mark(opacity=0.7)

            st.altair_chart(scatter, theme="streamlit", use_container_width=True)

# Team Data Page (no changes to Team Page, no count_input or z_val)
elif page == "Team Data":
    st.header('Team Data Analysis')
    st.markdown("**Statistics for all Conference Carolinas teams for the 2025 Men's Volleyball Season.**")

    # Create tabs for Scatter Plot and Bar Chart
    tab1, tab2 = st.tabs(['Scatter Plot', 'Bar Chart'])

    # Scatter Plot Tab
    with tab1:
        st.subheader("Scatter Plot Controls")

        # Select the x and y axis for teams
        x_val = st.selectbox("Pick your x-axis", filtered_team_data.select_dtypes(include=np.number).columns.tolist())
        y_val = st.selectbox("Pick your y-axis", filtered_team_data.select_dtypes(include=np.number).columns.tolist())

        # Check if x_val and y_val are different
        if x_val == y_val:
            st.warning("Please select different attributes for the x and y axes.")
        else:
            scatter = alt.Chart(filtered_team_data, title=f"{x_val} vs {y_val}").mark_point().encode(
                alt.X(x_val, title=f'{x_val}'),
                alt.Y(y_val, title=f'{y_val}'),
                color='Team',  # 'Team' can be used for categorical color encoding
                tooltip=['Team', x_val, y_val]
            ).configure_mark(
                opacity=0.7
            )

            st.altair_chart(scatter, theme="streamlit", use_container_width=True)

    # Bar Chart Tab
    with tab2:
        st.subheader("Bar Chart Controls")

        # Sidebar-like controls moved to the main area for this tab
        z_val = st.selectbox("Pick your attribute", filtered_team_data.select_dtypes(include=np.number).columns.tolist())

        # Dynamically adjust the number of teams shown based on the filtered data length
        top_data = filtered_team_data.nlargest(len(filtered_team_data), z_val)

        bar = alt.Chart(top_data).mark_bar().encode(
            y=alt.Y('Team', title='Team', sort='-x'),
            x=alt.X(z_val, title=f'{z_val}'),
            tooltip=['Team', z_val]
        ).properties(
            title=f"All Teams by {z_val}"
        ).configure_mark(
            opacity=0.7
        )

        st.altair_chart(bar, use_container_width=True)
