"""Main frotend for an app."""
import streamlit as st
import requests
import pandas as pd
import numpy as np
from gpt import GPT


class App():
    """Main frotend for an app."""
    def generate_frontend(self):
        # `st.set_page_config` is used to display the default layout width, 
        # the title of the app, and the emoticon in the browser tab.

        st.set_page_config(
            layout="centered", 
            page_title="Quiz creator!", page_icon="❄️"
        )

        ############ CREATE THE LOGO AND HEADING ############

        st.title("Examify")
        st.header("Most intelligent quiz creator in the world!")


        # We need to set up session state via st.session_state so 
        # that app interactions don't reset the app.

        if not "valid_inputs_received" in st.session_state:
            st.session_state["valid_inputs_received"] = False


        ############ TABBED NAVIGATION ############
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
                Let **AI** create for you quiz/test on a given text!
                """
            )

            release_info = st.expander(f'Release Notes. Last updated date: 01.03.23')
            with release_info:
                st.write(' - First model version')

            with st.form(key="my_form"):

                # MAX_KEY_PHRASES is a variable that controls the number 
                # of phrases that can be pasted:
                # The default in this app is 50 phrases. This can be 
                # changed to any number you like.

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
                numQuestionQuery = st.slider(
                    "Enter number of questions",
                    min_value=2, max_value=10, value=4,
                    step=1, format="%i"
                )

                numAnswerOptions = st.slider(
                    "Enter number of possible options for a question",
                    min_value=2, max_value=8, step=1, value=4,
                    format="%i"
                )

                questionDifficulty = st.selectbox(
                    'Select questions difficulty',
                    options=["easy", "medium", "hard"],
                    format_func=lambda x: x.capitalize()
                )

                submit_button = st.form_submit_button(label="Generate")

            ############ CONDITIONAL STATEMENTS ############

            # Now, let us add conditional statements to check if users have entered valid inputs.
            # E.g. If the user has pressed the 'submit button without text, 
            # without labels, and with only one label etc.
            # The app will display a warning message.
            if not submit_button and not st.session_state.valid_inputs_received:
                st.stop()

            elif submit_button and not userQuery:
                st.warning("❄️ There is no text.")
                st.session_state.valid_inputs_received = False
                st.stop()

            elif submit_button or st.session_state.valid_inputs_received:
                if submit_button:
                    # The block of code below if for our session state.
                    # This is used to store the user's inputs so that they 
                    # can be used later in the app.

                    st.session_state.valid_inputs_received = True

                ############ MAKING THE API CALL ############
                api_output = self.__run_gpt(userQuery,
                                            numQuestionQuery=numQuestionQuery,
                                            numAnswerOptions=numAnswerOptions,
                                            questionDifficulty=questionDifficulty)
                
                api_output = self.__answer_postprocessing(api_output)

                st.success("✅ Done!")
                st.caption("")
                st.markdown("### Check the results!")
                st.caption("")

                # Display the dataframe
                st.markdown(api_output)

    def __run_gpt(self,
                  prompt: str,
                  numQuestionQuery: int,
                  numAnswerOptions: int,
                  questionDifficulty: str) -> str:
        """Gets answer from OpenAPI GPT-3 model."""
        bot = GPT()
        answer = bot.get_answer(prompt,
                                numQuestionQuery=numQuestionQuery,
                                numAnswerOptions=numAnswerOptions,
                                questionDifficulty=questionDifficulty)
        return answer
    
    def __answer_postprocessing(self, api_output: str) -> str:
        """post process model output"""
        # add second spacing
        api_output = api_output.replace('\n', '\n\n')

        # make answering in Bold
        n_chars = len("Answer:")
        splitted_answer = api_output.split('\n\n')
        joined_answer = []
        for text_part in splitted_answer:
            if "answer:" in text_part.lower():
                formatted_text = (
                    "**" + text_part[:n_chars+2] + "**" + text_part[n_chars+2:]
                )
                joined_answer.append(formatted_text)
            else:
                joined_answer.append(text_part)
        formated_output = "\n\n".join(joined_answer)
        return formated_output

if __name__ == '__main__':
    app = App()
    app.generate_frontend()
