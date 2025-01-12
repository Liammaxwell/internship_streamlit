import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

# Read and prepare the data
players_data = pd.read_csv('2025 Conference Carolinas Player Stats.csv')

# Streamlit page configuration
st.set_page_config(layout="wide")
st.title('2025 Conference Carolinas Data Dashboard')

# Sidebar for navigation
page = st.sidebar.radio("Select a page", ["Player Data", "Team Data"])

# Team Filter in the Sidebar (Global filter) - Multi-Select for Teams
team_filter = st.sidebar.multiselect('Select Team(s) to Filter', ['All'] + players_data['Team'].unique().tolist(), default=['All'])

# Player Data Page
if page == "Player Data":
    st.header('Player Data Analysis')
    st.markdown("**Statistics for all Conference Carolinas players for the 2025 Men's Volleyball Season.**")

    # Create tabs for Scatter Plot and Bar Chart
    tab1, tab2 = st.tabs(['Scatter Plot', 'Bar Chart'])

    # Scatter Plot Tab
    with tab1:
        st.subheader("Scatter Plot Controls")

        # Sidebar-like controls moved to the main area for this tab
        # Filter dataset based on Team selection
        if 'All' not in team_filter:
            filtered_players_data = players_data[players_data['Team'].isin(team_filter)]
        else:
            filtered_players_data = players_data
        
        # Filter the players list based on the selected team(s)
        player = st.multiselect('Select players to compare', filtered_players_data['Name'])
        x_val = st.selectbox("Pick your x-axis", filtered_players_data.select_dtypes(include=np.number).columns.tolist())
        y_val = st.selectbox("Pick your y-axis", filtered_players_data.select_dtypes(include=np.number).columns.tolist())

        # Check if any player is selected and show the filtered data
        if player:
            filtered_players_data = filtered_players_data[filtered_players_data['Name'].isin(player)]
            st.dataframe(filtered_players_data)

            scatter = alt.Chart(filtered_players_data, title=f"{x_val} vs {y_val}").mark_point().encode(
                alt.X(x_val, title=f'{x_val}'),
                alt.Y(y_val, title=f'{y_val}'),
                color='Name',  # 'Name' can be used for categorical color encoding
                tooltip=['Name','Team','Position', x_val, y_val]
            ).configure_mark(
                opacity=0.7
            )

            st.altair_chart(scatter, theme="streamlit", use_container_width=True)
        else:
            st.warning("Please select players to compare.")

    # Bar Chart Tab
    with tab2:
        st.subheader("Bar Chart Controls")

        # Sidebar-like controls moved to the main area for this tab
        z_val = st.selectbox("Pick your attribute", players_data.select_dtypes(include=np.number).columns.tolist())
        count_input = st.number_input(f"Enter a value for the number of top {z_val} values to display", min_value=1, max_value=len(players_data), value=10, step=1)

        # Filter dataset based on Team selection
        if 'All' not in team_filter:
            filtered_players_data = players_data[players_data['Team'].isin(team_filter)]
        else:
            filtered_players_data = players_data

        top_data = filtered_players_data.nlargest(count_input, z_val)
        bar = alt.Chart(top_data).mark_bar().encode(
            y=alt.Y('Name', title='Name', sort='-x'),
            x=alt.X(z_val, title=f'{z_val}'),
            tooltip=['Name','Team','Position', z_val]
        ).properties(
            title=f"Top {count_input} Players by {z_val}"
        ).configure_mark(
            opacity=0.7
        )

        st.altair_chart(bar, use_container_width=True)

# Team Data Page (currently blank)
elif page == "Team Data":
    st.header('Team Data')
    st.markdown("**This page will be populated with team-related data in the future. Stay tuned!**")
