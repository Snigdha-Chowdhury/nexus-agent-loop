from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

llm = ChatGroq(model="openai/gpt-oss-20b")
def critic(draft_summary: str) -> str:
    prompt=f"Be a critique for this draft and find all the possible weaknesses:\n\n{draft_summary}"
    response=llm.invoke([HumanMessage(content=prompt)])
    return response.content