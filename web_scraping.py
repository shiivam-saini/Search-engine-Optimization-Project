from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_community.llms.ollama import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

import os

llama_model=Ollama(model="llama3")


os.environ['USER_AGENT'] = 'myagent'

def load_and_transform(url):
    loader = AsyncChromiumLoader([url])

    # Load the HTML asynchronously
    html =loader.load()

    # Check if HTML was loaded correctly
    if not html:
        print("Error: Failed to load HTML")
        return

    # Transform the HTML with BeautifulSoup
    bst = BeautifulSoupTransformer()
    docs_transformed = bst.transform_documents(html, tags_to_extract=["p","span"])

    if not docs_transformed:
        print("Error: No documents transformed")
        return
    
    return docs_transformed



def extract_keywords(result):
    prompt_template = PromptTemplate(input_variables=["result"], template="Extract the 20 most important SEO keywords from the following content: \n\n{result}")
    llm_chain = LLMChain(llm=llama_model, prompt=prompt_template)
    response=llm_chain.invoke({"result":result})

    keywords=response["text"]

    return keywords


def scrape_and_extract(url):
    result = load_and_transform(url)

    if result:
        keywords=extract_keywords(result)
        print(f"Extracted Keywords : {keywords}")
    else:
        print("Error: Failed to extract keywords")


url="https://www.cricbuzz.com/"
scrape_and_extract(url)


