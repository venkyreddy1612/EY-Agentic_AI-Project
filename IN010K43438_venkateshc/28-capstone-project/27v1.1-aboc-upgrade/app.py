# """
# Final entry point for ABOC system
# """

# import sys
# import os

# # Fix import issues
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# from graph.workflow import build_workflow
# from tools.database_tool import init_db


# def main():
#     print("\n🚀 ABOC AGENTIC SYSTEM (ADVANCED VERSION)\n")

#     # Initialize DB
#     init_db()

#     # Build workflow
#     app = build_workflow()

#     while True:
#         user_input = input("\nEnter your request (or 'exit'): ")

#         if user_input.lower() == "exit":
#             break

#         result = app.invoke({
#             "user_input": user_input
#         })

#         print("\n" + "=" * 50)
#         print("✅ FINAL RESULT")
#         print("=" * 50)

#         for key, value in result.items():
#             print(f"{key}: {value}")


# if __name__ == "__main__":
#     main()
import sys
import os
from dotenv import load_dotenv

# ---------------------------------------------------
# Fix imports + load environment variables
# ---------------------------------------------------

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.append(CURRENT_DIR)

load_dotenv()

# ---------------------------------------------------
# Imports
# ---------------------------------------------------

import streamlit as st

from graph.workflow import build_workflow
from tools.database_tool import init_db

# ---------------------------------------------------
# Page Config
# ---------------------------------------------------

st.set_page_config(
    page_title="ABOC Co-Pilot",
    page_icon="🚀",
    layout="wide"
)

# ---------------------------------------------------
# Header
# ---------------------------------------------------

st.title("🚀 Autonomous Business Operations Co-Pilot")

st.markdown("### Enter a business request:")

# ---------------------------------------------------
# Debug Section (temporary)
# ---------------------------------------------------

with st.expander("Debug Info"):

    groq_key = os.getenv("GROQ_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    st.write("GROQ_API_KEY Loaded:", groq_key is not None)
    st.write("OPENAI_API_KEY Loaded:", openai_key is not None)

# ---------------------------------------------------
# Input
# ---------------------------------------------------

user_input = st.text_input(
    "Business Request",
    value="Create a PO for 50 sensors from VendorA under 400000 INR",
    label_visibility="collapsed"
)

# ---------------------------------------------------
# Run Workflow
# ---------------------------------------------------

if st.button("Run Workflow"):

    if not user_input.strip():
        st.warning("Please enter a request.")
    else:

        try:

            # Spinner
            with st.spinner("Running agent workflow..."):

                # Initialize database
                init_db()

                # Build workflow
                app = build_workflow()

                # Invoke workflow
                result = app.invoke({
                    "user_input": user_input
                })

            # Success
            st.success("Workflow completed successfully")

            st.divider()

            st.subheader("📋 Final Result")

            # Display results nicely
            if isinstance(result, dict):

                for key, value in result.items():

                    st.markdown(f"### {key}")

                    if isinstance(value, (dict, list)):
                        st.json(value)
                    else:
                        st.write(value)

            else:
                st.write(result)

        except Exception as e:

            st.error(f"API Error: {str(e)}")

            st.exception(e)