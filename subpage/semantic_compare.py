import ast
import os
import streamlit as st
from abstract_page import SemanthaBasePage
from data.read_config import read_config

__config_path = os.path.join("semantic_compare", "config.toml")
CONFIG = read_config(__config_path)


class SemanticCompare(SemanthaBasePage):
    def __init__(self):
        super().__init__("🦸🏼‍♀️ Direct Semantic Compare")
        self.__models = ast.literal_eval(CONFIG["models"]["ids"])
        self.__compare_domain = CONFIG["domain"]["name"]

    def build(self):
        st.markdown("## Direct Compare")
        st.write(
            "Directly compare two texts by entering them below. The texts will be compared using semantha's® semantic model. The similarity score is a value between 0 and 1. The higher the score, the more similar the texts are."
        )
        curr_model = st.selectbox(
            "Which model would you like to use?", (self.__models.keys())
        )
        with st.spinner("Changing the model. Just a second..."):
            _ = self._semantha_connector.change_model(
                self.__compare_domain, self.__models[curr_model]
            )
        input_0 = st.text_input(label="Input I", value="I like to eat apples.")
        input_1 = st.text_input(label="Input II", value="I like to eat bananas.")
        __do_omd = st.checkbox(
            "Check whether similar sentence have an opposite meaning.", value=False
        )
        _, col, _ = st.columns([1, 1, 1])
        if col.button("⇆ Semantic Compare", key="scbutton"):
            with st.spinner("Wait for it..."):
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
