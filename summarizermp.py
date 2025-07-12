import operator
import asyncio
import os
from typing import Annotated, List, Literal, TypedDict
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_groq import ChatGroq
from langgraph.constants import Send
from langgraph.graph import START, END, StateGraph
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.combine_documents.reduce import acollapse_docs, split_list_of_docs
from dotenv import load_dotenv
load_dotenv()


llm = ChatGroq(
    model="llama3-8b-8192",
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY")
)


map_prompt = ChatPromptTemplate.from_messages([
    ("system", "Write a concise summary of the following:\n\n{context}")
])

reduce_template = """
The following is a set of summaries:
{docs}
Take these and distill it into a final, consolidated summary of the main themes.
"""
reduce_prompt = ChatPromptTemplate.from_messages([
    ("human", reduce_template)
])

text_splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=300, chunk_overlap=0)
token_max = 1000

def length_function(documents: List[Document]) -> int:
    return sum(llm.get_num_tokens(doc.page_content) for doc in documents)

class OverallState(TypedDict):
    contents: List[str]
    summaries: Annotated[list, operator.add]
    collapsed_summaries: List[Document]
    final_summary: str

class SummaryState(TypedDict):
    content: str

async def generate_summary(state: SummaryState):
    prompt = map_prompt.invoke(state["content"])
    response = await llm.ainvoke(prompt)
    return {"summaries": [response.content]}

def map_summaries(state: OverallState):
    return [Send("generate_summary", {"content": content}) for content in state["contents"]]

def collect_summaries(state: OverallState):
    return {
        "collapsed_summaries": [Document(page_content=summary) for summary in state["summaries"]]
    }

async def _reduce(input: dict) -> str:
    prompt = reduce_prompt.invoke(input)
    response = await llm.ainvoke(prompt)
    return response.content

async def collapse_summaries(state: OverallState):
    doc_lists = split_list_of_docs(state["collapsed_summaries"], length_function, token_max)
    results = []
    for doc_list in doc_lists:
        results.append(await acollapse_docs(doc_list, _reduce))
    return {"collapsed_summaries": results}

def should_collapse(state: OverallState) -> Literal["collapse_summaries", "generate_final_summary"]:
    num_tokens = length_function(state["collapsed_summaries"])
    return "collapse_summaries" if num_tokens > token_max else "generate_final_summary"

async def generate_final_summary(state: OverallState):
    response = await _reduce(state["collapsed_summaries"])
    return {"final_summary": response}


def run_chain(docs: List[Document]) -> str:
    split_docs = text_splitter.split_documents(docs)
    chain = create_stuff_documents_chain(llm, map_prompt)
    result = chain.invoke({"context": split_docs})
    return result


def load_and_summarize_url(url: str) -> dict:
    loader = WebBaseLoader(url)
    docs = loader.load()
    chain_summary = run_chain(docs)
    return {
        "chain_summary": chain_summary
    }


