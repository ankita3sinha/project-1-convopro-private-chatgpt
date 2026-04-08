from llama_index.core import PromptTemplate

from llm_factory.get_llm import get_ollama_llm

def get_title(model, user_query):
    llm = get_ollama_llm(model)
    title_prompt_template = ("You are a helpful assistant for generating concise titles for user queries. \n\n"
                             "Task - Read a given user query. Create a title of max 7 words.\n"
                             "Keep it professional and easy to understand\n\n"
                             "User query: \n{user_query}\n"
                             "Output: \nTitle: ")
    title_prompt = PromptTemplate(title_prompt_template).format(user_query=user_query)
    title = llm.complete(prompt=title_prompt).text
    return title