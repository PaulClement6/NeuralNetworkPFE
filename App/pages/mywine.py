import streamlit as st
from st_supabase_connection import SupabaseConnection

st.title("Tes bouteilles précedements scannées.")
conn = st.connection("supabase",type=SupabaseConnection)

# Perform query.
rows = conn.query("*", table="vins", ttl="10m").eq("Date","2001").execute()

# Print results.
for row in rows.data:
    st.write(f"Nom : {row['Nom']} / Date :{row['Date']}")
