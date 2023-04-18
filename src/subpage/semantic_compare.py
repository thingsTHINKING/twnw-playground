import ast
import os
import streamlit as st
from src.abstract_page import SemanthaBasePage
from data.read_config import read_config

__config_path = os.path.join("semantic_compare", "config.toml")
CONFIG = read_config(__config_path)


class SemanticCompare(SemanthaBasePage):
    def __init__(self):
        super().__init__("🦸🏼‍♀️ Semantic Compare")
        self.__models = ast.literal_eval(CONFIG["models"]["ids"])
        self.__compare_domain = CONFIG["domain"]["name"]

    def build(self):
        st.write(
            "Directly compare two texts in any language by entering them below. The texts will be compared using semantha's® semantic model. The similarity score is a value between 0 and 100. The higher the score, the more similar the texts are."
        )
        curr_model = st.selectbox(
            "Which model would you like to use?",
            (self.__models.keys()),
            help="Select a model to use for the comparison. Each model has a different accuracy and speed.",
        )
        with st.spinner("Changing the model. Just a second..."):
            _ = self._semantha_connector.change_model(
                self.__compare_domain, self.__models[curr_model]
            )
        input_0 = st.text_input(
            label="Input I",
            value="I like to eat apples.",
            help="Enter the first text to compare.",
        )
        input_1 = st.text_input(
            label="Input II",
            value="I like to eat bananas.",
            help="Enter the second text to compare.",
        )
        __do_omd = st.checkbox(
            "Opposite Meaning Detection",
            value=False,
            help="Check whether similar sentence have an opposite meaning.",
        )
        _, col, _ = st.columns([1, 1, 1])
        if col.button("⇆ Semantic Compare", key="scbutton"):
            with st.spinner("🦸🏼‍♀️ I am comparing your inputs..."):
                self.compute_and_display_similarity(input_0, input_1, __do_omd)

    def compute_and_display_similarity(
        self, input_0: str, input_1: str, __do_omd: bool
    ):
        similarity = self._semantha_connector.do_semantic_string_compare(
            input_0, input_1, self.__compare_domain
        )
        sim = int(round(similarity, 2) * 100)
        __omd = (
            False
            if not __do_omd
            else self._semantha_connector.get_opposite_meaning(
                input_0, input_1, self.__compare_domain
            )
        )
        if sim >= 70:
            if __do_omd and __omd:
                st.success(
                    f"🦸🏼‍♀️ The texts are {sim}% similar but have an **opposite meaning**."
                )
            else:
                st.success(f"🦸🏼‍♀️ The texts are {sim}% similar.")
        elif 70 > sim > 40:
            st.warning(f"🦸🏼 The texts are {sim}% similar.")
        elif sim <= 40:
            st.error("🦸🏼‍♀️ The texts are not similar.")
        st.metric("Semantic Similarity", f"{sim}")
