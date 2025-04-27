from langchain_community.utilities import SerpAPIWrapper
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain_community.llms import openai
from langchain.chat_models import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor, initialize_agent, AgentType
import os
import re
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain.agents import Tool
import speech_recognition as sr


# gemini-1.5-pro
load_dotenv()

class AiTutor:
    def __init__(self):

        client = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=os.getenv("GEMINI_API"))

        self.llm = client

        self.search = SerpAPIWrapper(
            search_engine="google",
            serpapi_api_key=os.getenv("SERP_API")
        )

        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            output_key="output",
            input_key="topic",
            return_messages=True
        )

        self.tools = [
            Tool(
                name="Google_Search",
                func=self.search.run,
                description="Useful for searching the web for information."
            )
        ]

    def tutor(self, topic):

        prompt = ChatPromptTemplate.from_messages([
                ("system", 
                    """
                    You are a helpful AI tutor. You will be given a question and you will answer it in a way that is easy to understand.
                    If you don't know the answer, say 'I don't know' or 'I'm not sure'. The questions will revolve around high school math, science, history, geography, home science, and others.
                    If the question is too complex, break it down into smaller parts and answer each part separately.
                    If the question is too simple, provide additional information or context to help the user understand the topic better.
                    If the question is too vague, ask the user for clarification or more details.
                    If the question is too specific, provide a general answer and suggest the user to do more research on the topic.
                    If the question is too long, summarize it and answer the main points.
                    Also, provide a summary of the topic and a list of resources or tools that can be used to learn more about the topic.
                    Provide examples and visual aids to help the user understand the topic better.
                    If the question is out of learning scope, say I can't help you with that.
                    
                    \"\"\"
                    Topic: {topic}
                    \"\"\"
                    """
                ),
                
                ("user", "{topic}"),
                ("placeholder", "{agent_scratchpad}"),
            ])


        print("Initializing agent...")

        
        # Initialize the agent with the tools and prompt
        agent = create_tool_calling_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )

        agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            return_intermediate_steps=False
        )
        if not topic:
            return "Please enter a topic."

        response = agent_executor.invoke({"topic": topic})
        text = response.get("output")

        return text

        # if isinstance(response, dict) and "output" in response:
        #     return response["output"]
           
    
        # else:
        #     return str(response)


    def clean_text_for_speech(self,text):
        # Remove asterisks, markdown, and extra whitespace
        text = re.sub(r"\*+", "", text)  # remove asterisks
        text = re.sub(r"_+", "", text)  # remove underscores
        text = re.sub(r"\[.*?\]\(.*?\)", "", text)  # remove markdown links
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def show_memory_status(self):
        return self.memory.chat_memory.messages
    

       
    