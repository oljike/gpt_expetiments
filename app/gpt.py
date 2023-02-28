import openai
openai.api_key = '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'


class GPT(object):
    def __init__(self):

        self.COMPLETIONS_MODEL = "text-davinci-003"
        self.EMBEDDING_MODEL = "text-embedding-ada-002"



    def get_answer(self, prompt, numQuestionQuery):

        if prompt is None or prompt=='':
            return "Input some text, please!"

        if numQuestionQuery.isdigit():
            numQuestionQuery = int(numQuestionQuery)
        else:
            numQuestionQuery = 4

        init_prompt = "As an advanced chatbot, your primary goal is to write {} difficult questions " \
                           "to the given text and 4 answer options in each and no correct options.\n\n".format(numQuestionQuery)

        return openai.Completion.create(
            prompt = init_prompt + prompt,
            temperature=1,
            max_tokens=300,
            model=self.COMPLETIONS_MODEL
        )["choices"][0]["text"].strip(" \n")
