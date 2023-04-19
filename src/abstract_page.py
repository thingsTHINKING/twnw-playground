from abc import ABC, abstractmethod
import streamlit as st

from semantha.SemanthaConnector import SemanthaConnector


class AbstractPage(ABC):
    def __init__(self, name):
        self.__name = name

    @abstractmethod
    def build(self):
        raise NotImplementedError

    @abstractmethod
    def __page_description(self):
        raise NotImplementedError

    def name(self):
        return self.__name


class SemanthaBasePage(AbstractPage, ABC):
    def __init__(self, name):
        super().__init__(name)
        self._semantha_connector = SemanthaConnector(
            server_base_url=st.secrets["semantha"]["server_url"],
            streamlit_domains_prefix=st.secrets["semantha"]["domain_prefix"],
            api_key=st.secrets["semantha"]["api_key"],
        )
