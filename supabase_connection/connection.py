from streamlit.connections import ExperimentalBaseConnection
from streamlit.runtime.caching import cache_data

import streamlit as st
import supabase
import pandas as pd

class SUPABASECONNECTION(ExperimentalBaseConnection[supabase.Client]):
    def __init__(self, st_module, **kwargs):
        super().__init__(**kwargs)
        self.st = st_module

    def _connect(self, **kwargs) -> supabase.Client:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return supabase.create_client(url, key)
    
    @cache_data(ttl=3600)
    def _select(self, table,function, ttl: int = 3600, **kwargs):
    
        client = self._connect()
        #result=client.table(table).select(function).execute()
        #if function is a list convert it into stringd seperated by a comma
        if isinstance(function, list):
            function = ', '.join(function)
        result=client.table(table).select(function).execute()
        return result
    
    @cache_data(ttl=3600)
    def _select_filter(self, table,function, column,operator,criteria, ttl: int = 3600, **kwargs):
        client = self._connect()
        if isinstance(function, list):
            function = ', '.join(function)
        result=client.table(table).select(function).filter(column=column,operator=operator,criteria=criteria).execute()
        return result
    
    @cache_data(ttl=3600)
    def _insert(self, table, data, ttl: int = 3600, **kwargs):
        client = self._connect()
        result=client.table(table).insert(data).execute()
        return result
    
    @cache_data(ttl=3600)
    def _update(self, table, data,row_id ,ttl: int = 3600, **kwargs):
        client = self._connect()
        result=client.table(table).update(data).eq("id",row_id).execute()
        return result
