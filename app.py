import streamlit as st
import psycopg2
import pandas as pd

# Function to connect to the database
def connect_to_db():
    """Connect to the PostgreSQL database using Streamlit secrets."""
    try:
        connection = psycopg2.connect(
            host=st.secrets["database"]["host"],
            database=st.secrets["database"]["dbname"],
            user=st.secrets["database"]["user"],
            password=st.secrets["database"]["password"],
            port=st.secrets["database"]["port"]
        )
        print(host)
        return connection
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
        return None

def execute_query(connection, query):
    """Execute a user-provided SQL query and return the results as a Pandas DataFrame."""
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        # Fetch results if the query is a SELECT statement
        if query.strip().lower().startswith("select"):
            columns = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()
            df = pd.DataFrame(data, columns=columns)
            return df
        else:
            # For non-SELECT queries, commit the changes
            connection.commit()
            return "Query executed successfully."
    except Exception as e:
        return f"Error executing query: {e}"

def main():
    st.title("UHC data Extractor")

    st.write("### Enter your SQL query below:")

    # SQL query input
    user_query = st.text_area("SQL Query", placeholder="Enter your SQL query here...")

    if st.button("Execute"):
        if user_query.strip():
            # Connect to the database
            connection = connect_to_db()
            if connection:
                # Execute the query
                result = execute_query(connection, user_query)
                if isinstance(result, pd.DataFrame):
                    st.write("### Query Results")
                    st.dataframe(result)  # Display the results as a table
                else:
                    st.write(result)  # Display success or error message
                connection.close()
            else:
                st.error("Unable to connect to the database.")
        else:
            st.error("Please enter a valid SQL query.")

if __name__ == "__main__":
    main()
