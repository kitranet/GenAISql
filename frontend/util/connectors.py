import pandas as pd
from sqlalchemy import create_engine, inspect
from sqlalchemy.schema import CreateTable, MetaData
import urllib.parse
import pyodbc
import logging
import util.logging as ul

appLogger = logging.getLogger('frontend')

# class PostgresqlConnector:
#     def __init__(self,hostname,port,username,password,database):
#         self.type = 'postgresql'
#         self.username = username
#         self.password = urllib.parse.quote_plus(password)
#         self.hostname = hostname
#         self.port = port
#         self.database = database
#         self.conn_string = f'postgresql+psycopg2://{self.username}:{self.password}@{self.hostname}:{self.port}/{self.database}'
#         self.engine = create_engine(self.conn_string)
#         self.metadata = None
#         self.selected_metadata_key = None
#     def get_results(self,sql):
#         result = pd.read_sql(sql,con=self.engine)
#         return result
#     def list_tables(self):
#         inspector = inspect(self.engine)
#         out_tab = []
#         schemas = inspector.get_schema_names()
#         for schema in schemas:
#             for table_name in inspector.get_table_names(schema=schema):
#                 out_tab.append(schema+'.'+table_name)
#         return out_tab
#     def extract_metadata(self):
#         # out_list = []
#         # meta = MetaData()
#         # meta.reflect(bind=self.engine)
#         # for table in meta.sorted_tables:
#         #     out_list.append(f"{table}.{table.schema}({table.c})")
#         inspector = inspect(self.engine)
#         out_list = {}
#         schemas = inspector.get_schema_names()
#         for schema in schemas:
#             self.selected_metadata_key = schema
#             out_list [f"{schema}"] = {}
#             for table_name in inspector.get_table_names(schema=schema):
#                 try:
#                     columns = inspector.get_columns(table_name)
#                 except Exception as e:
#                     continue
#                 out_list [f"{schema}"][f"{schema}.{table_name}"] = [column['name'] for column in columns]
#                 # out_list.append(f"{schema}.{table_name}({','.join([column['name'] for column in columns])})")
#         print(out_list)
#         self.metadata = out_list
#         # return f'Instruction: Use {self.type} table structure to write querries\n'+'\n'.join(out_list)
#     def fetch_metadata(self):
#         selected_metadata = self.metadata[self.selected_metadata_key]
        

#     def __del__(self):
#         self.engine.dispose()

class MSSqlConnector:
    def __init__(self,hostname,port,username,password,database,active_dir = True,name='noname'):
        self.type = 'MS SQL'
        self.name = name
        self.username = username
        self.password = password
        self.hostname = hostname
        self.port = port
        self.database = database
        con_params = urllib.parse.quote_plus(f"Driver={'{'}ODBC Driver 18 for SQL Server{'}'};Server={self.hostname};Port={self.port};DATABASE={self.database};UID={self.username};PWD={self.password}"+(";Authentication=ActiveDirectoryPassword" if active_dir else ""))
        self.conn_string = "mssql+pyodbc:///?odbc_connect=%s" % con_params
        self.engine = create_engine(self.conn_string)
        # self.metadata = self.fetch_metadata()
        self.metadata = None
        self.selected_entities = None
    def get_results(self,sql):
        result = pd.read_sql(sql,con=self.engine)
        return result
    def fetch_metadata(self):
        out_list = {}
        output = self.get_results("SELECT table_schema, table_name, column_name From INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA NOT IN ('sys')")
        for index, row in output.iterrows():
            input_key = f"{row['table_schema'].upper()}.{row['table_name'].upper()}"
            if input_key in out_list.keys():
                out_list[input_key].append(row['column_name'].lower())
            else:
                out_list[input_key] = [row['column_name'].lower()]
        self.metadata = out_list
        self.selected_entities = out_list.keys()
        print(out_list)
    def format_metadata(self):
        if not self.metadata:
            raise Exception(f"metadata does not exist for: {self.name}")
        out_list = '\n'.join([f"{key}({','.join(self.metadata[key])})" for key in self.selected_entities])
        return f'Instruction: Use {self.type} table structure to write querries. Only these tables are present in the databse.\\n{out_list}\n'
    def get_metadata(self):
        if not self.metadata:
            raise Exception(f"metadata does not exist for: {self.name}")
        return {ele: self.metadata[ele] for ele in self.selected_entities}
    def get_selected_schema_names(self):
        return set([key.split('.')[0] for key in self.metadata.keys()]), set([ele.split('.')[0] for ele in self.selected_entities])
    def set_selected_schema_names(self, selected_schemas):
        selected_entities = []
        for key in self.metadata.keys():
            if key.split('.')[0] in selected_schemas:
                selected_entities.append(key)
        self.selected_entities = selected_entities
    def __del__(self):
        self.engine.dispose()

class MSAccessConnector:
    def __init__(self,db_path):
        self.type = 'access'
        self.db_path = db_path
        self.conn_string = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};' \
                                f'DBQ={self.db_path};'
        self.conn = pyodbc.connect(self.conn_string)
        self.fetch_metadata = self.fetch_metadata()
    def get_results(self,sql):
        result = pd.read_sql(sql,con=self.conn)
        return result
    def list_tables(self):
        return [table.table_name for table in self.conn.cursor().tables(tableType='TABLE')]
    def fetch_metadata(self):
        return ""
    def __del__(self):
        self.conn.close()