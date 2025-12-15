import json
import sqlite3
import pandas as pd
import xml.etree.ElementTree as ET
import yaml


class Outputs:
    @staticmethod
    def all_sers() -> None:
        Outputs.json_ser()
        Outputs.csv_ser()
        Outputs.xml_ser()
        Outputs.yaml_ser()

    @staticmethod
    def json_ser() -> None:
        with sqlite3.connect('database.db') as con:
            con.row_factory = sqlite3.Row
            cursor = con.cursor()
            result = {}
            tables = [table[0] for table in cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall() if not table[0].startswith('sqlite_')]
            for table in tables:
                result[table] = list([dict(row) for row in cursor.execute(f"SELECT * FROM {table}").fetchall()])
        with open('out/data.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=4, ensure_ascii=False)

    @staticmethod
    def csv_ser() -> None:
        with sqlite3.connect('database.db') as con:
            cursor = con.cursor()
            tables = [table[0] for table in cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall() if not table[0].startswith('sqlite_')]
            for table in tables:
                df = pd.read_sql_query(f"SELECT * FROM {table}", con) # type: ignore
                df.to_csv(f'out/{table}.csv', index=False, encoding='utf-8')

    @staticmethod
    def xml_ser() -> None:
        with sqlite3.connect('database.db') as con:
            cursor = con.cursor()
            tables = [table[0] for table in cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall() if not table[0].startswith('sqlite_')]
            root = ET.Element('database') # type: ignore
            for table in tables:
                df = pd.read_sql_query(f"SELECT * FROM {table}", con) # type: ignore
                table_elem = ET.SubElement(root, 'table', name=table) # type: ignore
                for _, row in df.iterrows():
                    record_elem = ET.SubElement(table_elem, 'record') # type: ignore
                    for col in df.columns:
                        if pd.notna(row[col]):
                            col_elem = ET.SubElement(record_elem, col) # type: ignore
                            col_elem.text = str(row[col])
            tree = ET.ElementTree(root) # type: ignore
            ET.indent(tree, space='    ')
            tree.write('out/data.xml', encoding='utf-8', xml_declaration=True) # type: ignore

    @staticmethod
    def yaml_ser() -> None:
        with sqlite3.connect('database.db') as con:
            con.row_factory = sqlite3.Row
            cursor = con.cursor()
            tables = [table[0] for table in cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall() if not table[0].startswith('sqlite_')]
            result = {}
            for table in tables:
                table_data = []
                rows = cursor.execute(f"SELECT * FROM {table}").fetchall()
                for row in rows:
                    row_dict = {}
                    for key in row.keys():
                        value = row[key]
                        row_dict[key] = value
                    table_data.append(row_dict) # type: ignore
                result[table] = table_data    
            with open('out/data.yaml', 'w', encoding='utf-8') as f:
                yaml.dump(result, f, allow_unicode=True, default_flow_style=False)
