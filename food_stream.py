import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import plotly.express as px
import re
import subprocess
import os, sys

#  Database Configuration 
DB_USER = st.secrets["DB_USER"]
DB_PASS = st.secrets["DB_PASS"]
DB_HOST = st.secrets["DB_HOST"]
DB_PORT = st.secrets["DB_PORT"]
DB_NAME = st.secrets["DB_NAME"]

# Create DB connection
engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

def run_bootstrap_processes():
    # Run bootstrap SQL scripts
    SQL_FILE = "Dataset/FoodLFWMS.sql"  # SQL file path

    with open(SQL_FILE, "r") as f:
        sql_script = f.read()

    queries = [q.strip() for q in sql_script.split(';') if q.strip()]

    bootstrap_results = {}

    with engine.begin() as conn:
        for i, query in enumerate(queries):
            try:
                conn.execute(text(query))
                if query.lower().startswith("select"):
                    df = pd.read_sql(text(query), conn)
                    bootstrap_results[f"Query_{i+1}"] = df
            except Exception as e:
                pass

    # Additional bootstrap for data wrangling
    DATA_WRANGLING_SQL = "Dataset/data_wrangling.sql"

    with open(DATA_WRANGLING_SQL, "r") as f:
        wrangling_script = f.read()

    wrangling_queries = [q.strip() for q in wrangling_script.split(';') if q.strip()]


    with engine.begin() as conn:
        for query in wrangling_queries:
            conn.execute(text(query))

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATASET_DIR = os.path.join(BASE_DIR, "..", "Dataset")
    importdata_path = os.path.join(DATASET_DIR, "importcsv.py")
    cleandata_path = os.path.join(DATASET_DIR, "cleandata.py")
    subprocess.run([sys.executable, importdata_path], check=True)
    subprocess.run([sys.executable, cleandata_path], check=True)


# Initialize session state for section
if "section" not in st.session_state:
    st.session_state["section"] = "Home"
section = st.sidebar.radio(
    "Go to",
    ["Home", "SQL Queries & Results", "Add New Record", "Delete Record"],
    index=["Home", "SQL Queries & Results", "Add New Record", "Delete Record"].index(st.session_state["section"])
)

#  Page logic based on selected section 
if section == "Home":
    st.title("Local Food Wastage Management System")
    st.write("""
    ## Project Overview
When I first started building the Local Food Wastage Management System, my goal was to create a platform that could connect food providers like restaurants, grocery stores, and even households with recipients like NGOs, food banks, and community centers. 
The idea was to reduce waste by making surplus food easily accessible to those who need it most.

It is a fully interactive, database connected system that not only enables redistribution but also cleans, updates, and visualizes the data in real time.
I also added automatic data cleaning in the process. 
Now, whenever I insert or delete a record, names are properly formatted, contact numbers are standardized, and statuses are kept consistent. 
This makes sure the database stays clean and analytics remain trustworthy without constant manual intervention.

I added SQL Queries & Results section that cover everything from city wise provider and receiver counts to food type distribution, claim success rates, and wastage tracking. To make the data more engaging, I integrated Plotly bar charts that shows the query’s output whether it’s a simple two column result or something more complex that needs grouped bars.

Managing the data is easier with the Update Database section, where I can run cleaning scripts, manually edit records, and even export cleaned datasets in a tab separated format. 
The Add New Record feature lets me insert new rows into any table, while automatically applying the same cleaning logic before saving. 
I also added a Delete Record section for safely removing outdated or incorrect entries.

### Objectives:
- To minimize food wastage by redistributing excess food from providers to those in need.
- To build a user-friendly platform that allows food providers to list available surplus food items.
- To enable recipients to claim and schedule pickups or deliveries of surplus food.
- To track food listings, claims, and distribution status to ensure transparency and accountability.
- To promote community engagement and raise awareness about sustainable food consumption practices.

### System Charts:
- Total Providers count in each city
- Total Receivers count in each city
- Food provider contribution for distribution
- First POC for food providers in each city
- Receivers who have claimed the most food
- Total quantity of food available from all providers
- Food listing providers by type of food
- Top 10 food providers
- Most commonly available Food type
- Food claims made for each food item
- Provider with highest number of successful claims
- Provider with successful food category
- Food claims percentage
- Average quantity of food claimed by receiver
- Status count of Meal_Type
- Most claimed Meal_type
- Quantity of food donated by each provided
- Quantity of food donated by each provided by food_type
- Food Wastage in each city

### Impacts & Benefits
- As a developer, I found that implementing the Local Food Wastage Management System provided valuable insights into the intersection of technology and social good. Building the platform required thoughtful design of database schemas, user interfaces, and logic to ensure both providers and recipients could interact seamlessly.
- The project emphasized the importance of transparency and traceability in food redistribution, which not only builds trust but also enables better data-driven decisions for all stakeholders.
- Personally, I learned how technology can be leveraged to address real-world challenges like food insecurity and environmental sustainability, and how collaborative efforts between communities and technologists can create meaningful impact.

### Conclusion
- The Local Food Wastage Management System demonstrates how digital solutions can bridge the gap between surplus and need, fostering a more sustainable and equitable food ecosystem.
- Ongoing engagement, maintenance, and feature enhancements will be crucial for the platform’s continued success and broader adoption.
- This project has reinforced my commitment to using my technical skills for societal benefit, and I look forward to exploring further innovations in this domain.

### Presented by:
# Karthik Doguparthi
    """)

elif section == "SQL Queries & Results":

    # Re-run the wrangling SQL before loading queries
    DATA_WRANGLING_SQL = "Dataset/data_wrangling.sql"
    with open(DATA_WRANGLING_SQL, "r") as f:
        wrangling_script = f.read()
    wrangling_queries = [q.strip() for q in wrangling_script.split(';') if q.strip()]
    with engine.begin() as conn:
        for query in wrangling_queries:
            conn.execute(text(query))

    st.title("SQL Queries & Results")

    SQL_FILE = "Dataset/FoodLFWMS.sql"  # SQL file path

    with open(SQL_FILE, "r") as f:
        sql_script = f.read()

    queries = [q.strip() for q in sql_script.split(';') if q.strip()]

    tabs = st.tabs([f"Query {i+1}" for i in range(len(queries))])

    for i, query in enumerate(queries):
        with tabs[i]:
            st.subheader(f"Query {i+1}")
            st.code(query, language="sql")
            try:
                with engine.connect() as conn:
                    df = pd.read_sql(text(query), conn)
                st.dataframe(df)

                # Plot bar chart
                if df.shape[1] == 2:
                    # Simple bar chart
                    x_col = df.columns[0]
                    y_col = df.columns[1]
                    fig = px.bar(df, x=x_col, y=y_col, title=f"{x_col} vs {y_col}")
                    st.plotly_chart(fig, use_container_width=True)

                elif df.shape[1] >= 3:
                    # Grouped bar chart
                    fig = px.bar(df, x=df.columns[0], y=df.columns[2], color=df.columns[1], 
                                barmode='group', title=f"{df.columns[0]} by {df.columns[1]}")
                    st.plotly_chart(fig, use_container_width=True)

                else:
                    st.info("Chart not auto-configured for this number of columns.")

            except Exception as e:
                st.error(f"Error running query: {e}")
                st.write("Please check the SQL syntax or database connection.")

# Add New Record Section
elif section == "Add New Record":
    st.title("Add New Record to a Table")

    # Cleaning helper functions
    def clean_name(val):
        return val.strip().replace(",", "").replace(".", "").replace(";", "")

    def clean_contact(val):
        val = val.strip()
        val = val.lstrip("0")  # Remove leading zeros
        if len(val) >= 10 and val.isdigit():
            return f"+1 ({val[0:3]}) {val[3:6]}-{val[6:10]}"
        return val

    def clean_status(val):
        return val.strip().lower()

    try:
        with engine.connect() as conn:
            tables_df = pd.read_sql("SHOW TABLES", conn)
            tables = tables_df.iloc[:,0].tolist()
    except Exception as e:
        st.error(f"Error fetching tables: {e}")
        tables = []

    selected_table = st.selectbox("Select Table", tables) if tables else None

    if selected_table:
        try:
            with engine.connect() as conn:
                schema_df = pd.read_sql(f"DESCRIBE {selected_table}", conn)
        except Exception as e:
            st.error(f"Error fetching schema: {e}")
            schema_df = None

        if schema_df is not None:
            # Identify input columns (skip auto_increment primary key)
            input_columns = []
            for _, row in schema_df.iterrows():
                if "auto_increment" in str(row["Extra"]).lower():
                    continue
                input_columns.append(row["Field"])

            st.markdown(f"### Enter values for new record in `{selected_table}`")

            new_record = {}
            for col in input_columns:
                new_record[col] = st.text_input(f"{col}")

            if st.button("Insert Record"):
                if any(v.strip() == "" for v in new_record.values()):
                    st.error("Please fill in all fields before inserting.")
                else:
                    # Apply cleaning rules based on column name
                    for col in new_record:
                        if "name" in col.lower():
                            new_record[col] = clean_name(new_record[col])
                        elif "contact" in col.lower():
                            new_record[col] = clean_contact(new_record[col])
                        elif "status" in col.lower():
                            new_record[col] = clean_status(new_record[col])
                        else:
                            new_record[col] = new_record[col].strip()

                    try:
                        cols_str = ", ".join(input_columns)
                        vals_str = ", ".join([f":{col}" for col in input_columns])
                        insert_query = text(f"INSERT INTO {selected_table} ({cols_str}) VALUES ({vals_str})")
                        with engine.begin() as conn:
                            conn.execute(insert_query, new_record)
                        st.success("Record inserted and cleaned successfully!")
                    except Exception as e:
                        st.error(f"Error inserting record: {e}")

#Delete Record Section    
elif section == "Delete Record":
    st.title("Delete Record from a Table")

    tables = ["providers_data", "receivers_data", "food_listings_data", "claims_data"]
    selected_table = st.selectbox("Select Table", tables)

    try:
        df = pd.read_sql(f"SELECT * FROM {selected_table}", engine)
    except Exception as e:
        st.error(f"Error fetching data from {selected_table}: {e}")
        df = None

    if df is not None and not df.empty:
        id_col = df.columns[0]  # assuming first column is the primary key
        selected_id = st.selectbox(f"Select {id_col} to delete", df[id_col].unique())

        if st.button("Delete Record"):
            try:
                delete_query = text(f"DELETE FROM {selected_table} WHERE {id_col} = :id_val")
                with engine.begin() as conn:
                    conn.execute(delete_query, {"id_val": selected_id})
                st.success(f"Record with {id_col}={selected_id} deleted successfully!")
            except Exception as e:
                st.error(f"Error deleting record: {e}")
    else:
        st.info(f"No records found in {selected_table}.")