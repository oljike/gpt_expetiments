import openai
openai.api_key = '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'


class GPT(object):
    COMPLETIONS_MODEL = "text-davinci-003"
    EMBEDDING_MODEL = "text-embedding-ada-002"

    def get_answer(self, prompt: str,
                   numQuestionQuery: int,
                   numAnswerOptions: int,
                   questionDifficulty: str):

        if prompt is None or prompt=='':
            return "Input some text, please!"

        init_prompt = (
            f"""
            As an advanced chatbot, your primary goal is to write {numQuestionQuery} 
            questions with {questionDifficulty} difficulty 
            to the given text and {numAnswerOptions} answer options 
            in each and one of them is correct. Make sure that answers options written in alphavital order. 
            Add correct answer in the end of each section. Also, don't include order of answer between questions.\n\n
        """
        )

        return openai.Completion.create(
            prompt = init_prompt + prompt,
            temperature=1,
            max_tokens=300,
            model=self.COMPLETIONS_MODEL
        )["choices"][0]["text"].strip(" \n")
