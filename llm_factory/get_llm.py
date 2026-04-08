from llama_index.llms.ollama import Ollama
from config.settings import Settings

settings = Settings()

OLLAMA_URL = settings.OLLAMA_URL

_current_model_name = None
_current_llm_instance = None

def get_ollama_llm(model_name: str):
    global _current_model_name, _current_llm_instance
    if(_current_model_name == model_name):
        return _current_llm_instance
    llm = Ollama(base_url=OLLAMA_URL, model = model_name)
    _current_model_name = model_name
    _current_llm_instance = llm
    return _current_llm_instance

#check_llm = get_ollama_llm(model_name= "gemma2:2b")
#print(check_llm)
#print(type(check_llm))
