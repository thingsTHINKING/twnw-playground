import streamlit as st
import pandas as pd
from abstract_page import SemanthaBasePage


class SemanticSearchSemantha(SemanthaBasePage):
    def __init__(self):
        super().__init__("🔍 Semantic Search")

    def build(self):
        use_case = self.use_case_selection()
        search_string = st.text_input(label="Search", value="Men and Women are equal.")
        _, _, col_2, _, _ = st.columns(5)
        self.compute_matches(col_2, search_string, use_case)
        self.display_library(col_2, use_case)

    def compute_matches(self, col_2, search_string, use_case):
        if col_2.button("🔍 Search"):
            with st.spinner("🦸🏼‍♀️ I am searching for matches..."):
                # TODO: delete when paragraph matching is implemented
                if use_case == 'PG_Search_Constitutions':
                    results = self._semantha_connector.query_library(
                        search_string, use_case, threshold=0.40, tags=['paragraph']
                    )
                else:
                    results = self._semantha_connector.query_library(
                        search_string, use_case, threshold=0.40
                    )
            st.success("Done! Here are your matches!", icon='🦸🏼‍♀️')
            self.display_matches(results)

    def display_matches(self, results):
        with st.expander("Matches", expanded=True):
            matches = self.get_matches(results)
            st.markdown(matches.to_markdown(), unsafe_allow_html=True)
            st.markdown("", unsafe_allow_html=True)

    def display_library(self, col_2, use_case):
        if col_2.button("📖 Library"):
            with st.expander("First 100 entries"):
                # TODO: only fot workshop
                if use_case == 'PG_Search_Constitutions':
                    lib = self._semantha_connector.get_library(use_case, tags=['full_text'], limit=100)
                else:
                    lib = self._semantha_connector.get_library(use_case, limit=100)
                lib_df = pd.DataFrame.from_records(
                    [[r["doc_name"], r["content"].replace("\n", "<br>")] for r in lib],
                    columns=["Name", "Content"],
                )
                lib_df.index = range(1, lib_df.shape[0] + 1)
                st.table(lib_df)

    def get_matches(self, results):
        matches = pd.DataFrame.from_records(
            [
                [
                    r["doc_name"],
                    r["content"].replace("\n", "<br>"),
                    int(round(r["similarity"], 2) * 100),
                ]
                for r in list(results.values())
            ],
            columns=["Name", "Content", "Similarity"],
        )
        matches.index = range(1, matches.shape[0] + 1)
        matches.index.name = "Rank"
        return matches

    def use_case_selection(self):
        st.write('Select a library to search in. We provide a row of pre-filled libraries with various use cases. Take a look:')
        domains = self._semantha_connector.get_streamlit_domains()
        option = st.selectbox("Library:", domains)
        return option
