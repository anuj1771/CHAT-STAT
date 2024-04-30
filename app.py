import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt



def render_home_page():
    st.sidebar.title("Whatsapp chat Analyzer")

    uploaded_file = st.sidebar.file_uploader("choose a file")

    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8")
        df = preprocessor.preprocess(data)
        return df



def render_about_page(df):
    # fetch unique users
    if df is not None:
        user_list = df['user'].unique().tolist()
        user_list.remove('group_notification')
        user_list.sort()
        user_list.insert(0,"Overall")

        selected_user = st.sidebar.selectbox("Show analysis ",user_list)

        # word cloud
        st.title("WordCloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.imshow(df_wc)
        st.pyplot(fig)

        # if st.sidebar.button("Show Analysis"):

        num_messages,words,num_media_messages,num_links = helper.fetch_stats(selected_user,df)
        st.markdown("<h1 style='font-family: Arial, sans-serif;font-size: 70px;text-align: center;'>Top Statistics</h1>", unsafe_allow_html=True)

        col1, col2 ,col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)

        # monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots(figsize=(5, 3))
        ax.plot(timeline['time'], timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.title("Activity Map")
        col1,col2 =st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig,ax = plt.subplots(figsize=(5, 3))
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots(figsize=(5, 3))
            ax.bar(busy_month.index, busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # finding the busiest users in th group(Group level)
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots(figsize=(5, 3))
            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)



        #most common words
        most_common_df = helper.most_common_words(selected_user,df)

        fig,ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])

        st.title('mostCommon Words')
        st.pyplot(fig)
        #st.dataframe(most_common_df)

        # emoji analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")
        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)

        # most common message
        most_common_msg = helper.most_common_messages(selected_user, df)

        fig, ax = plt.subplots()
        ax.barh(most_common_msg[0], most_common_msg[1])

        st.title('mostCommon Messages')
        st.pyplot(fig)
        st.title('Negative Messages')
        # Negative messages

        x1, new_df1 = helper.negative_msg(df)
        fig, ax = plt.subplots()
        col1, col2 = st.columns(2)

        with col1:
            ax.bar(new_df1['user'], new_df1['Negative_Score'], color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.dataframe(new_df1[['user','Negative_Score','message']])

def render_about_page2(df):
    if df is not None:
        user_list = df['user'].unique().tolist()
        user_list.remove('group_notification')
        user_list.sort()
        user_list.insert(0, "Overall")

        selected_user = st.sidebar.selectbox("Show analysis ", user_list)

        if st.sidebar.button("Show Analysis"):
            num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
            st.markdown("<h1 style='font-family: Arial, sans-serif;font-size: 70px;text-align: center;'>Top Statistics</h1>", unsafe_allow_html=True)

            # Total Statistics
            st.header("Total Statistics")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Messages", num_messages)
            with col2:
                st.metric("Total Words", words)
            with col3:
                st.metric("Media Shared", num_media_messages)
            with col4:
                st.metric("Links Shared", num_links)

            # Monthly Timeline
            st.title("Monthly Timeline")
            fig, ax = plt.subplots(figsize=(10, 5))
            timeline = helper.monthly_timeline(selected_user, df)
            ax.plot(timeline['time'], timeline['message'], color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

            # Daily Timeline
            st.title("Daily Timeline")
            fig, ax = plt.subplots(figsize=(10, 5))
            daily_timeline = helper.daily_timeline(selected_user, df)
            ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

            # Activity Map
            st.title("Activity Map")
            col1, col2 = st.columns(2)
            with col1:
                st.header("Most busy day")
                busy_day = helper.week_activity_map(selected_user, df)
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.bar(busy_day.index, busy_day.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.header("Most busy Month")
                busy_month = helper.month_activity_map(selected_user, df)
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.bar(busy_month.index, busy_month.values, color='orange')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            # Most Busy Users
            if selected_user == 'Overall':
                st.title('Most Busy Users')
                x, new_df = helper.most_busy_users(df)
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
                st.dataframe(new_df)

            # Word Cloud
            st.title("WordCloud")
            df_wc = helper.create_wordcloud(selected_user, df)
            st.image(df_wc, use_column_width=True)

            # Most Common Words
            st.title('Most Common Words')
            most_common_df = helper.most_common_words(selected_user, df)
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.barh(most_common_df[0], most_common_df[1])
            st.pyplot(fig)

            # Emoji Analysis
            st.title("Emoji Analysis")
            emoji_df = helper.emoji_helper(selected_user, df)
            st.dataframe(emoji_df)

            # Most Common Messages
            st.title('Most Common Messages')
            most_common_msg = helper.most_common_messages(selected_user, df)
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.barh(most_common_msg[0], most_common_msg[1])
            st.pyplot(fig)

            # Negative Messages
            st.title('Negative Messages')
            x1, new_df1 = helper.negative_msg(df)
            col1, col2 = st.columns(2)
            with col1:
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.bar(new_df1['user'], new_df1['Negative_Score'], color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df1[['user', 'Negative_Score', 'message']])
# ***********************************************************************************************************************

import streamlit as st
import sqlite3
import hashlib

# Function to create a database connection
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn

# Function to create a new user table
def create_table(conn):
    sql_create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        file_data BLOB
    );
    """

    try:
        c = conn.cursor()
        c.execute(sql_create_users_table)
    except sqlite3.Error as e:
        print(e)

# Function to hash the password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to check if a user exists
def user_exists(conn, username):
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    return c.fetchone() is not None

# Function to authenticate a user
def authenticate_user(conn, username, password):
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hash_password(password)))
    return c.fetchone() is not None

def get_file_data(conn, username):
    c = conn.cursor()
    c.execute("SELECT file_data FROM users WHERE username=?", (username,))
    row = c.fetchone()
    return row[0] if row else None
# // **************************************************************************************************


def main():
    conn = create_connection("users.db")
    if conn is not None:
        # Create users table if it doesn't exist
        create_table(conn)

        # Sidebar option for login, signup, or file upload
        option = st.sidebar.radio("Choose an option", ("Login", "Signup", "Logout"))

        if option == "Signup":
            st.sidebar.subheader("Signup")
            new_username = st.sidebar.text_input("Username")
            new_password = st.sidebar.text_input("Password", type="password")
            # uploaded_file = st.sidebar.file_uploader("Upload a text file")

            uploaded_file = st.sidebar.file_uploader("choose a file")






            if st.sidebar.button("Signup"):
                if user_exists(conn, new_username):
                    st.sidebar.error("Username already exists!")
                else:
                    hashed_password = hash_password(new_password)
                    file_data = " "
                    if uploaded_file is not None:
                        file_data = uploaded_file.getvalue().decode("utf-8")

                    c = conn.cursor()
                    c.execute("INSERT INTO users (username, password, file_data) VALUES (?, ?, ?)",
                              (new_username, hashed_password, file_data))
                    conn.commit()
                    st.sidebar.success("Signup successful! You can now login.")

        elif option == "Login":
            st.sidebar.subheader("Login")
            username = st.sidebar.text_input("Username")
            password = st.sidebar.text_input("Password", type="password")

            if st.sidebar.button("Login"):
                if authenticate_user(conn, username, password):
                    st.success(f"Welcome back, {username}!")
                    data = get_file_data(conn, username)
                    df = preprocessor.preprocess(data)
                    render_about_page(df)
                else:
                    st.error("Invalid username or password.")

        elif option == "Logout":
            # Clear session data or display a logout message
            st.success("You have been logged out successfully.")

    else:
        st.error("Failed to connect to the database.")

    # params = st.experimental_get_query_params()
    # page = params.get("page", ["home"])[0]

    # data = c.fetchone()[0]
    # df = preprocessor.preprocess(data)
    # # df = render_home_page()
    # render_about_page2(df)

if __name__ == "__main__":
    main()


