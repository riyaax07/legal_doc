import os as OS
import utils as Utils

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory


class NewsChat:
    store = {}

    def __init__(self, session_id: str):
        self.session_id = session_id

        openai_key = OS.getenv("OPENAI_API_KEY")

        # Embeddings
        embeddings = OpenAIEmbeddings(
            openai_api_key=openai_key,
            model="text-embedding-3-small"
        )

        # Vector DB
        vectordb = Chroma(
            persist_directory=Utils.DB_FOLDER,
            embedding_function=embeddings,
            collection_name="collection_1"
        )

        retriever = vectordb.as_retriever()

        # LLM
        llm = ChatOpenAI(
            openai_api_key=openai_key,
            model="gpt-4o",
            temperature=0
        )

        # -------- History-aware retriever prompt --------
        contextualize_prompt = ChatPromptTemplate.from_messages([
            ("system",
             "Given the chat history and the latest user question, "
             "rewrite the question so it is standalone."),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}")
        ])

        history_aware_retriever = create_history_aware_retriever(
            llm, retriever, contextualize_prompt
        )

        # -------- QA prompt --------
        qa_prompt = ChatPromptTemplate.from_messages([
            ("system",
             "You are an assistant for EU AI law questions. "
             "Use the provided context to answer concisely. "
             "If you do not know, say so.\n\n{context}"),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}")
        ])

        qa_chain = create_stuff_documents_chain(llm, qa_prompt)

        rag_chain = create_retrieval_chain(
            history_aware_retriever,
            qa_chain
        )

        # -------- Runnable with memory --------
        self.rag_chain = RunnableWithMessageHistory(
            rag_chain,
            self.get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )

    # -------- Chat memory --------
    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        if session_id not in self.store:
            self.store[session_id] = ChatMessageHistory()
        return self.store[session_id]

    # ✅ THIS IS THE METHOD YOU WERE MISSING
    def ask(self, question: str) -> str:
        result = self.rag_chain.invoke(
            {"input": question},
            config={"configurable": {"session_id": self.session_id}},
        )
        return result["answer"]
