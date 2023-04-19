import streamlit as st
import pandas as pd
from src.abstract_page import SemanthaBasePage


class SemanticSearch(SemanthaBasePage):
    DOMAIN_IDENTIFIER = "PG_Search_"

    def __init__(self):
        super().__init__("🔍 Semantic Search")

    def build(self):
        self.page_description()
        use_case, search_string = self.__search_form()
        self.__compute_matches(search_string, use_case)
        self.__display_library(use_case)

    def page_description(self):
        st.write(
            "I have a library of documents from various domains. You can search for your query in my library and I "
            "will find the most similar entries for any language."
        )

    def __search_form(self):
        with st.expander("🔍 Search", expanded=True):
            use_case = self.__use_case_selection()
            search_string = st.text_input(
                label="Query",
                value="Men and Women are equal.",
                help="Enter your search query and I will find the most similar entries in my library.",
            )

        return use_case, search_string

    def __compute_matches(self, search_string, use_case):
        _, _, col, _, _ = st.columns(5)
        if col.button("🔍 Search"):
            with st.spinner("🦸🏼‍♀️ I am searching for matches..."):
                if use_case == self.DOMAIN_IDENTIFIER + "Constitutions":
                    results = self._semantha_connector.query_library(
                        search_string, use_case, threshold=0.40, tags=["paragraph"]
                    )
                else:
                    results = self._semantha_connector.query_library(
                        search_string, use_case, threshold=0.40
                    )
            st.success("Done! Here are your matches!", icon="🦸🏼‍♀️")
            self.__display_matches(results)

    def __display_matches(self, results):
        with st.expander("Matches", expanded=True):
            matches = self.__get_matches(results)
            st.write(matches)

    def __display_library(self, use_case):
        _, _, col, _, _ = st.columns(5)
        if col.button("📖 Library"):
            with st.expander("First 100 entries", expanded=True):
                if use_case == self.DOMAIN_IDENTIFIER + "Constitutions":
                    lib = self._semantha_connector.get_library(
                        use_case, tags=["full_text"], limit=100
                    )
                else:
                    lib = self._semantha_connector.get_library(use_case, limit=100)
                lib_df = pd.DataFrame.from_records(
                    [[r["doc_name"], r["content"].replace("\n", "<br>")] for r in lib],
                    columns=["Name", "Content"],
                )
                lib_df.index = range(1, lib_df.shape[0] + 1)
                st.write(lib_df)

    def __use_case_selection(self):
        domains = self._semantha_connector.get_streamlit_domains()
        domains = [d.replace(self.DOMAIN_IDENTIFIER, "") for d in domains]
        option = st.selectbox(
            "Library:",
            domains,
            help="We have prepared some libraries for you and filled them with documents from various domains. You can "
            "select one of them here and search for your query.",
        )
        return self.DOMAIN_IDENTIFIER + option

    @staticmethod
    def __get_matches(results):
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
