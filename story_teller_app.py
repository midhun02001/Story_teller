import os
import streamlit as st
import google.generativeai as genai
import pyperclip  # New import for clipboard handling

def main():
    # Set your Gemini API key directly here
    api_key = 'AIzaSyA3_ihH3RnaZG2aoGbcspP26c-W8vKf5To'
    genai.configure(api_key=api_key)

    # Set up the Streamlit interface
    st.title("Story Teller")

    # User input for story content description
    user_input = st.text_area(
        "Please describe the story you want to generate (e.g., 'A fantasy adventure with a dragon and a brave knight')",
        height=200
    )

    # Button to generate story
    if st.button("Generate Story"):
        if user_input.strip():
            # Create a prompt for generating the story content
            prompt = f"""
            Based on the following description, please generate a creative story:

            "{user_input}"

            The story should have a clear beginning, middle, and end, and include imaginative elements to engage the reader.
            """

            try:
                # Use the Gemini generative model to generate the story content
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(prompt)
                story_body = response.text

                # Store the generated story in the session state to keep it persistent
                st.session_state.generated_story = story_body
                st.session_state.copy_status = "Copy Story to Clipboard"  # Reset the copy button text

            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.warning("We couldn't generate the story. Please try again later.")
        else:
            st.warning("Please provide a description of the story content.")

    # Check if the generated story is in session state
    if 'generated_story' in st.session_state:
        st.subheader("Your Generated Story:")
        story_text_area = st.text_area("Generated Story:", st.session_state.generated_story, height=400, key="story_content")

        # Button to copy story to clipboard
        if st.button(st.session_state.get('copy_status', "Copy Story to Clipboard")):
            try:
                # Use pyperclip to copy the text to the clipboard
                pyperclip.copy(st.session_state.generated_story)
                st.session_state.copy_status = "COPIED"
                st.success("Story copied to clipboard!")
            except Exception as e:
                st.error(f"Failed to copy to clipboard: {e}")

if __name__ == "__main__":
    main()
