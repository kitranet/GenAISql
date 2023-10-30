import pandas as pd
from sqlalchemy import create_engine, inspect
from sqlalchemy.schema import CreateTable, MetaData
import urllib.parse
import pyodbc

class PostgresqlConnector:
    def __init__(self,hostname,port,username,password,database):
        self.type = 'postgresql'
        self.username = username
        self.password = urllib.parse.quote_plus(password)
        self.hostname = hostname
        self.port = port
        self.database = database
        self.conn_string = f'postgresql+psycopg2://{self.username}:{self.password}@{self.hostname}:{self.port}/{self.database}'
        self.engine = create_engine(self.conn_string)
        self.metadata = self.get_metadata()
    def get_results(self,sql):
        result = pd.read_sql(sql,con=self.engine)
        return result
    def list_tables(self):
        inspector = inspect(self.engine)
        out_tab = []
        schemas = inspector.get_schema_names()
        for schema in schemas:
            for table_name in inspector.get_table_names(schema=schema):
                out_tab.append(schema+'.'+table_name)
        return out_tab
    def get_metadata(self):
        # out_list = []
        # meta = MetaData()
        # meta.reflect(bind=self.engine)
        # for table in meta.sorted_tables:
        #     out_list.append(f"{table}.{table.schema}({table.c})")
        inspector = inspect(self.engine)
        out_list = []
        schemas = inspector.get_schema_names()
        for schema in schemas:
            for table_name in inspector.get_table_names(schema=schema):
                try:
                    columns = inspector.get_columns(table_name)
                except Exception as e:
                    continue
                out_list.append(f"{schema}.{table_name}({','.join([column['name'] for column in columns])})")
        print(out_list)
        return f'Instruction: Use {self.type} table structure to write querries\n'+'\n'.join(out_list)
    def __del__(self):
        self.engine.dispose()

class MSSqlConnector:
    def __init__(self,hostname,port,username,password,database,active_dir = True):
        self.type = 'MS SQL'
        self.username = username
        self.password = password
        self.hostname = hostname
        self.port = port
        self.database = database
        con_params = urllib.parse.quote_plus(f"Driver={'{'}ODBC Driver 18 for SQL Server{'}'};Server={self.hostname};Port={self.port};DATABASE={self.database};UID={self.username};PWD={self.password}"+(";Authentication=ActiveDirectoryPassword" if active_dir else ""))
        self.conn_string = "mssql+pyodbc:///?odbc_connect=%s" % con_params
        self.engine = create_engine(self.conn_string)
        self.metadata = self.get_metadata()
    def get_results(self,sql):
        result = pd.read_sql(sql,con=self.engine)
        return result
    def list_tables(self):
        inspector = inspect(self.engine)
        out_tab = []
        schemas = inspector.get_schema_names()
        for schema in schemas:
            for table_name in inspector.get_table_names(schema=schema):
                out_tab.append(schema+'.'+table_name)
        return out_tab
    def get_metadata(self):
        # out_list = []
        # meta = MetaData()
        # meta.reflect(bind=self.engine)
        # for table in meta.sorted_tables:
        #     out_list.append(f"{table}.{table.schema}({table.c})")
        inspector = inspect(self.engine)
        out_list = []
        schemas = inspector.get_schema_names()
        for schema in schemas:
            for table_name in inspector.get_table_names(schema=schema):
                try:
                    columns = inspector.get_columns(table_name)
                except Exception as e:
                    continue
                out_list.append(f"{schema}.{table_name}({','.join([column['name'] for column in columns])})")
        print(out_list)
        return f'Instruction: Use {self.type} table structure to write querries\n'+'\n'.join(out_list)
    def __del__(self):
        self.engine.dispose()

class MSAccessConnector:
    def __init__(self,db_path):
        self.type = 'access'
        self.db_path = db_path
        self.conn_string = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};' \
                                f'DBQ={self.db_path};'
        self.conn = pyodbc.connect(self.conn_string)
        self.get_metadata = self.get_metadata()
    def get_results(self,sql):
        result = pd.read_sql(sql,con=self.conn)
        return result
    def list_tables(self):
        return [table.table_name for table in self.conn.cursor().tables(tableType='TABLE')]
    def get_metadata(self):
        return ""
    def __del__(self):
        self.conn.close()