############ 1. IMPORTING LIBRARIES ############

# Import streamlit, requests for API calls, and pandas and numpy for data manipulation

import streamlit as st
import requests
import pandas as pd
import numpy as np
from streamlit_tags import st_tags  # to add labels on the fly!
from gpt import GPT

############ 2. SETTING UP THE PAGE LAYOUT AND TITLE ############

# `st.set_page_config` is used to display the default layout width, the title of the app, and the emoticon in the browser tab.

st.set_page_config(
    layout="centered", page_title="Quiz creator!", page_icon="❄️"
)

############ CREATE THE LOGO AND HEADING ############

# We create a set of columns to display the logo and the heading next to each other.


# c1, c2 = st.columns([0.32, 2])
#
# # The snowflake logo will be displayed in the first column, on the left.
#
# with c1:
#
#     st.caption("")
#     st.title("Quiz creator!")
st.title("Quiz creator!")

# The heading will be on the right.
#
# with c2:
#
#     st.caption("")
#     st.title("Quiz creator!")


# We need to set up session state via st.session_state so that app interactions don't reset the app.

if not "valid_inputs_received" in st.session_state:
    st.session_state["valid_inputs_received"] = False


############ TABBED NAVIGATION ############

# First, we're going to     create a tabbed navigation for the app via st.tabs()
# tabInfo displays info about the app.
# tabMain displays the main app.

MainTab, InfoTab = st.tabs(["Main", "Info"])



with InfoTab:

    st.subheader("What is Examify?")
    st.markdown(
        "Examify will help you create a quiz or test based on given using AI!."
    )



with MainTab:

    # Then, we create a intro text for the app, which we wrap in a st.markdown() widget.

    st.write("")
    st.markdown(
        """
    Generete a quiz/test based on a given text using GPT!
    """
    )

    st.write("")

    # Now, we create a form via `st.form` to collect the user inputs.

    # All widget values will be sent to Streamlit in batch.
    # It makes the app faster!

    with st.form(key="my_form"):

        ############ ST TAGS ############

        # We initialize the st_tags component with default "labels"

        # Here, we want to classify the text into one of the following user intents:
        # Transactional
        # Informational
        # Navigational

        # labels_from_st_tags = st_tags(
        #     value=["Transactional", "Informational", "Navigational"],
        #     maxtags=3,
        #     suggestions=["Transactional", "Informational", "Navigational"],
        #     label="",
        # )

        # The block of code below is to display some text samples to classify.
        # This can of course be replaced with your own text samples.

        # MAX_KEY_PHRASES is a variable that controls the number of phrases that can be pasted:
        # The default in this app is 50 phrases. This can be changed to any number you like.

        MAX_KEY_PHRASES = 50

        new_line = "\n"

        # pre_defined_keyphrases = [
        #     "I want to buy something",
        #     "We have a question about a product",
        #     "I want a refund through the Google Play store",
        #     "Can I have a discount, please",
        #     "Can I have the link to the product page?",
        # ]
        #
        # # Python list comprehension to create a string from the list of keyphrases.
        # keyphrases_string = f"{new_line.join(map(str, pre_defined_keyphrases))}"
        keyphrases_string = ''
        # The b lock of code below displays a text area
        # So users can paste their phrases to classify

        userQuery = st.text_area(
            # Instructions
            "Enter the text",
            # 'sample' variable that contains our keyphrases.
            keyphrases_string,
            # The height
            height=200,
            # The tooltip displayed when the user hovers over the text area.
            help="Enter the text here",
            key="1",
        )
        # st.number_input("Enter number of questions", )
        numQuestionQuery = st.text_area(
            # Instructions
            "Enter number of questions",
            help="Enter number of question in digits",
            key="2",
        )

        # userQuery = userQuery.strip("\n")  # Converts the pasted text to a Python list
        submit_button = st.form_submit_button(label="Generate")

    ############ CONDITIONAL STATEMENTS ############

    # Now, let us add conditional statements to check if users have entered valid inputs.
    # E.g. If the user has pressed the 'submit button without text, without labels, and with only one label etc.
    # The app will display a warning message.

    if not submit_button and not st.session_state.valid_inputs_received:
        st.stop()

    elif submit_button and not userQuery:
        st.warning("❄️ There is no text.")
        st.session_state.valid_inputs_received = False
        st.stop()

    # elif submit_button and not labels_from_st_tags:
    #     st.warning("❄️ You have not added any labels, please add some! ")
    #     st.session_state.valid_inputs_received = False
    #     st.stop()
    #
    # elif submit_button and len(labels_from_st_tags) == 1:
    #     st.warning("❄️ Please make sure to add at least two labels for classification")
    #     st.session_state.valid_inputs_received = False
    #     st.stop()

    elif submit_button or st.session_state.valid_inputs_received:

        if submit_button:

            # The block of code below if for our session state.
            # This is used to store the user's inputs so that they can be used later in the app.

            st.session_state.valid_inputs_received = True

        ############ MAKING THE API CALL ############

        # First, we create a Python function to construct the API call.
        def run_gpt(prompt):
            bot = GPT()
            answer = bot.get_answer(prompt, numQuestionQuery)

            return answer

        api_output = run_gpt(userQuery)

        st.success("✅ Done!")

        st.caption("")
        st.markdown("### Check the results!")
        st.caption("")


        # Display the dataframe
        st.write(api_output)
