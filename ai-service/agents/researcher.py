from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

llm = ChatGroq(model="openai/gpt-oss-20b")
def research(topic: str) -> str:
    prompt=f"Research the following topic and provide detailed notes:\n\n{topic}"
    response=llm.invoke([HumanMessage(content=prompt)])
    return response.content