import ast
import os
import streamlit as st
from src.abstract_page import SemanthaBasePage
from data.read_config import read_config

__config_path = os.path.join("rag", "config.toml")
CONFIG = read_config(__config_path)


class RAG(SemanthaBasePage):
    def __init__(self):
        super().__init__("💬 Retrieval Augmented Generation")
        self.__use_cases = ast.literal_eval(CONFIG["domains"]["use_cases"])

    def build(self):
        self.page_description()
        self.__use_case_selection()

    def __use_case_selection(self):
        with st.expander("🔘 Use Case Selection", expanded=True):
            choice = st.selectbox(
                "Pick one use case from various domains", list(self.__use_cases.keys())
            )

            description = self.__use_cases[choice]["description"]
            st.write(description)

            link = self.__use_cases[choice]["link"]
            st.info(f"Click on the link to learn more about [{choice}]({link}).")

    def page_description(self):
        st.markdown(
            "While *Large Language Models* (LLMs) have shown impressive capabilities, they can sometimes generate **false or irrelevant information** and **fail** to make use of current and updated **internal knowledge**."
        )
        st.markdown(
            "With *Retrieval Augmented Generation* (RAG), we take a different approach, leveraging semantha®'s semantic search to retrieve highly relevant documents and generate answers **based solely on this information**. By avoiding the invention of new facts and drawing solely from a existing knowledge base, *RAG* provides a reliable and accurate tool for generating high-quality answers."
        )
        st.markdown(
            "Unlike others, all the processing is done in the EU and your **data remains private**. Try it out!"
        )
