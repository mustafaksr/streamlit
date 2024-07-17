import streamlit as st

st.write("""# Hello World """)
st.write("""## Hello World """)
          
st.write("""### Hello World""")


# Initialize connection.
conn = st.connection('mysql', type='sql')

# Perform query.
df = conn.query('SELECT * from wp_users;', ttl=600)

# Print results.
for row in df.itertuples():
    st.write(f"user_login : {row.user_login} |  user_pass : {row.user_pass}:")

st.write("# df")
st.dataframe(df)

st.write("# df columns")
st.dataframe(df[["user_login","user_pass"]])
