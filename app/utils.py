import os
import datetime
import openai
from langchain.llms import OpenAI
from langchain.agents import initialize_agent
# from langchain.agents.agent_toolkits import ZapierToolkit
# from langchain.utilities.zapier import ZapierNLAWrapper
from langchain.agents import Tool
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI

from langchain import LLMChain
from langchain.agents import Tool, AgentExecutor
from langchain.prompts.chat import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from langchain import PromptTemplate

import re

conversation = []

os.environ['OPENAI_API_KEY'] = ""
os.environ['HUGGINGFACEAPIKEY']=""

template_1 = """

Do not generate user responses on your own and avoid repeating questions.

You are a helpful scheduling assistant. Your only task is to help user schedule a service appointment with a bank.
Bank only provides these services: to create invoice, fetch invoice details. Bank is open from 8 am to 5 pm EST everyday and are available to book as long as it is open.
To create a invoice you need to collect information in the conservation such as invoice type, datetime, po number, total amount, total tax, items and quantity.
Collect all of the information one by one, and do not ask for service type again if user has stated it in the conversation before.
Allow users to input time in any format, and you'll save it in a EST 24-hours format in the backend to display at the end.
After collecting all of the information, make sure you display the details to the user at the end in this format:

invoice type:
datetime:
po number:
total amount:
total tax:
items:
quantity:

Respond with just 'Thank you for choosing us' at the end.

{chat_history}

"""

system_message_prompt = SystemMessagePromptTemplate.from_template(template_1)
human_template="{query}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt,human_message_prompt])

chat = ChatOpenAI(model="gpt-3.5-turbo",temperature=0.7)

memory = ConversationBufferMemory(memory_key="chat_history")

def gpt_response(query):

    chain = LLMChain(llm = chat, prompt = chat_prompt, memory = memory)
    response = chain.run(query)

    return response

import re

def extract_information(conversation, pattern):
    for line in conversation:
        match = re.search(pattern, line, re.IGNORECASE)
        if match:
            return match.group(1)
    return None