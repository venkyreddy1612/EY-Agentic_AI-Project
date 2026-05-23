# """
# Streamlit UI for ABOC system
# """

# import streamlit as st
# import requests

# API_URL = "http://localhost:8000/run"

# st.set_page_config(page_title="ABOC AI System", layout="wide")

# st.title("🚀 Autonomous Business Operations Co-Pilot")

# st.markdown("### Enter a business request:")

# user_input = st.text_input(
#     "Example: Create a PO for 50 sensors from VendorA under 400000 INR"
# )

# if st.button("Run Workflow"):

#     if user_input:
#         with st.spinner("Processing..."):

#             response = requests.post(API_URL, json={"query": user_input})

#             if response.status_code == 200:
#                 data = response.json()["result"]

#                 st.success("Workflow Completed!")

#                 st.subheader("📊 Output")

#                 for key, value in data.items():
#                     st.write(f"**{key}**: {value}")

#             else:
#                 st.error("API Error")
"""
Streamlit UI for ABOC system
"""

import streamlit as st
import requests

# ---------------------------------------------------
# Backend API URL
# ---------------------------------------------------

API_URL = "http://localhost:8000/run"

# ---------------------------------------------------
# Streamlit Page Config
# ---------------------------------------------------

st.set_page_config(
    page_title="ABOC AI System",
    layout="wide"
)

# ---------------------------------------------------
# Header
# ---------------------------------------------------

st.title("🚀 Autonomous Business Operations Co-Pilot")

st.markdown("### Enter a business request:")

# ---------------------------------------------------
# Input Box
# ---------------------------------------------------

user_input = st.text_input(
    "Business Request",
    placeholder="Example: Create a PO for 50 sensors from VendorA under 400000 INR"
)

# ---------------------------------------------------
# Run Workflow Button
# ---------------------------------------------------

if st.button("Run Workflow"):

    if not user_input.strip():

        st.warning("Please enter a request.")

    else:

        with st.spinner("Processing..."):

            try:

                # ---------------------------------------------------
                # API Request
                # ---------------------------------------------------

                response = requests.post(
                    API_URL,
                    json={
                        "query": user_input
                    }
                )

                # ---------------------------------------------------
                # Success Response
                # ---------------------------------------------------

                if response.status_code == 200:

                    response_json = response.json()

                    st.success("✅ Workflow Completed!")

                    st.subheader("📊 Output")

                    # Extract result safely
                    result = response_json.get("result", response_json)

                    # Display nicely
                    if isinstance(result, dict):

                        for key, value in result.items():

                            st.markdown(f"### {key}")

                            if isinstance(value, (dict, list)):
                                st.json(value)
                            else:
                                st.write(value)

                    else:
                        st.write(result)

                # ---------------------------------------------------
                # API Error Response
                # ---------------------------------------------------

                else:

                    st.error(f"❌ API Error ({response.status_code})")

                    try:
                        st.json(response.json())
                    except:
                        st.text(response.text)

            # ---------------------------------------------------
            # Connection Errors
            # ---------------------------------------------------

            except requests.exceptions.ConnectionError:

                st.error(
                    "❌ Cannot connect to backend API.\n\n"
                    "Make sure FastAPI server is running on port 8000."
                )

            # ---------------------------------------------------
            # General Errors
            # ---------------------------------------------------

            except Exception as e:

                st.error(f"❌ Unexpected Error: {str(e)}")

                st.exception(e)