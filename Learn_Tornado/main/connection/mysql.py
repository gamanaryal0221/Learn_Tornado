import pymysql
from ..src.code.utils.constants import Constants
MysqlDB = Constants.Config.MysqlDB


def get_connections(config):
    data_sources_key = Constants.Config.Key.MYSQL_DATA_SOURCES
    
    if data_sources_key in config:
        print('\n\n---------- Initializing database connection ----------')
        data_sources = config[data_sources_key]
        connections = {}

        learn_tornado1_key = MysqlDB.LEARN_TORNADO1
        connections[learn_tornado1_key] = get_connection_from_data_source(learn_tornado1_key, data_sources)

        learn_tornado2_key = MysqlDB.LEARN_TORNADO2
        connections[learn_tornado2_key] = get_connection_from_data_source(learn_tornado2_key, data_sources)

        return connections
    else:
        raise ConnectionError(f'Configuration not found for the data source connection')

def get_connection_from_data_source(data_source_key, data_sources):
    if data_source_key in data_sources:
        print(f'\nEstablishing datasource connection with \'{data_source_key}\' ...')
        connection = None
        try:
            data_source = data_sources[data_source_key]

            connection = pymysql.connect(
                host=data_source[MysqlDB.HOSTNAME],
                database=data_source[MysqlDB.DATABASE],
                user=data_source[MysqlDB.USER],
                password=data_source[MysqlDB.PASSWORD],
                autocommit=True
            )
        except Exception as e:
            print(e)

        if connection:
            print(f'Successfully established connection with \'{data_source_key}\'')
            return connection
        else:
            raise ConnectionError(f'Could not established connection with \'{data_source_key}\'')
        
    else:
        raise ConnectionError(f'Datasource not found for the connection with \'{data_source_key}\'')
    

class Sql():
    def get_connection(self, data_source_key):
        if data_source_key:
            mysql_connections = self.application.mysql_connections
            if data_source_key in mysql_connections:
                return mysql_connections[data_source_key]
            else:
                raise RuntimeError(f'Could not find mysql connection with data source key:{data_source_key}')
        else:
            raise ValueError('Null data source key received')
        
    def get_all_records_mapped(cursor, want_one_if_one=True):
        if cursor.rowcount > 0:
            print("\nRefining cursor data")
            all_data = cursor.fetchall()

            records = []
            columns = [column[0] for column in cursor.description]

            for data in all_data:
                record = dict(zip(columns, data))
                records.append(record)

            if len(records)==1 and want_one_if_one:
                return records[0]
            else:
                return records
        else:
            None