import requests
import streamlit as st

API_URL = "http://localhost:8000"

# Page title
st.title("🍵 Tea Manager")

# Tabs for actions
tabs = st.tabs(["View All", "Add Tea", "Update Tea", "Delete Tea"])

# View all teas
with tabs[0]:
    st.subheader("All Teas")
    response = requests.get(f"{API_URL}/teas")
    if response.status_code == 200:
        teas = response.json()
        if teas:
            for i in range(0, len(teas), 2):
                col1, col2 = st.columns(2)

                with col1:
                    tea = teas[i]
                    st.markdown(
                        f"""
                        <div style="
                            background: #2A7B9B;
                            background: linear-gradient(90deg, rgba(42, 123, 155, 1) 0%, rgba(87, 199, 133, 1) 50%, rgba(237, 221, 83, 1) 100%);
                            padding: 1rem;
                            margin-bottom: 1rem;
                            border-radius: 10px;
                            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                        ">
                            <h4 style="margin-bottom: 0.5rem;">{tea["name"]} <span style='color: #090979;'>({tea["type"]})</span></h4>
                            <p style="margin: 0;"><strong>ID:</strong> {tea.get("id", tea.get("_id"))}</p>
                            <p style="margin: 0;"><strong>Origin:</strong> {tea["origin"]}</p>
                            <p style="margin-top: 0.5rem;"><strong>Description:</strong><br>{tea["description"]}</p>
                        </div>
                    """,
                        unsafe_allow_html=True,
                    )

                # If there is a second tea in the pair
                if i + 1 < len(teas):
                    with col2:
                        tea = teas[i + 1]
                        st.markdown(
                            f"""
                            <div style="
                                background: #2A7B9B;
                                background: linear-gradient(90deg, rgba(42, 123, 155, 1) 0%, rgba(87, 199, 133, 1) 50%, rgba(237, 221, 83, 1) 100%);
                                padding: 1rem;
                                margin-bottom: 1rem;
                                border-radius: 10px;
                                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                            ">
                                <h4 style="margin-bottom: 0.5rem;">{tea["name"]} <span style='color: #090979;'>({tea["type"]})</span></h4>
                                <p style="margin: 0;"><strong>ID:</strong> {tea.get("id", tea.get("_id"))}</p>
                                <p style="margin: 0;"><strong>Origin:</strong> {tea["origin"]}</p>
                                <p style="margin-top: 0.5rem;"><strong>Description:</strong><br>{tea["description"]}</p>
                            </div>
                        """,
                            unsafe_allow_html=True,
                        )

        else:
            st.info("No teas found.")
    else:
        st.error("Failed to fetch teas.")

# Add a new tea
with tabs[1]:
    st.subheader("Add Tea")
    with st.form("add_form"):
        id = st.number_input("ID", min_value=1, step=1)
        name = st.text_input("Name")
        tea_type = st.text_input("Type")
        origin = st.text_input("Origin")
        description = st.text_area("Description")
        submitted = st.form_submit_button("Add Tea")
        if submitted:
            payload = {
                "id": id,
                "name": name,
                "type": tea_type,
                "origin": origin,
                "description": description,
            }
            res = requests.post(f"{API_URL}/teas", json=payload)
            if res.status_code == 200:
                st.success("Tea added successfully!")
            else:
                st.error("Failed to add tea.")

# Update a tea
with tabs[2]:
    st.subheader("Update Tea")
    tea_id = st.text_input("Tea ID to Update")
    with st.form("update_form"):
        id = st.number_input("ID", min_value=1, step=1)
        name = st.text_input("New Name")
        tea_type = st.text_input("New Type")
        origin = st.text_input("New Origin")
        description = st.text_area("New Description")
        submitted = st.form_submit_button("Update")
        if submitted:
            update_payload = {
                "id": id,
                "name": name,
                "type": tea_type,
                "origin": origin,
                "description": description,
            }
            res = requests.put(f"{API_URL}/teas/{tea_id}", json=update_payload)
            if res.status_code == 200:
                st.success("Tea updated successfully!")
            else:
                st.error("Failed to update tea. Check the ID.")

# Delete a tea
with tabs[3]:
    st.subheader("Delete Tea")
    delete_id = st.text_input("Tea ID to Delete")
    if st.button("Delete"):
        res = requests.delete(f"{API_URL}/teas/{delete_id}")
        if res.status_code == 200:
            st.success("Tea deleted successfully.")
        else:
            st.error("Failed to delete tea. Check the ID.")
