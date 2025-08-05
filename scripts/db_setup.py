# scripts/db_setup.py
import mysql.connector
from mysql.connector import errorcode

DB_CONFIG = {
    'user': 'root',
    'password': 'mesh1234',
    'host': '127.0.0.1',
    'port': 3306
}
DB_NAME = 'fsmw_db'

TABLES = {}
TABLES['pastas'] = (
    "CREATE TABLE `pastas` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `nome` varchar(255) NOT NULL,"
    "  `caminho_completo` text NOT NULL,"
    "  `id_pai` int(11) DEFAULT NULL,"
    "  PRIMARY KEY (`id`),"
    "  UNIQUE KEY `caminho_completo_idx` (`caminho_completo`(767)),"
    "  KEY `id_pai` (`id_pai`),"
    "  CONSTRAINT `pastas_ibfk_1` FOREIGN KEY (`id_pai`) REFERENCES `pastas` (`id`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

TABLES['arquivos'] = (
    "CREATE TABLE `arquivos` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `nome_arquivo` varchar(255) NOT NULL,"
    "  `caminho_completo` text NOT NULL,"
    "  `tamanho_bytes` bigint(20) NOT NULL,"
    "  `data_modificacao` datetime NOT NULL,"
    "  `id_pasta` int(11) NOT NULL,"
    "  PRIMARY KEY (`id`),"
    "  UNIQUE KEY `caminho_completo_idx` (`caminho_completo`(767)),"
    "  KEY `id_pasta` (`id_pasta`),"
    "  CONSTRAINT `arquivos_ibfk_1` FOREIGN KEY (`id_pasta`) REFERENCES `pastas` (`id`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

def create_database(cursor):
    try:
        cursor.execute(f"CREATE DATABASE {DB_NAME} DEFAULT CHARACTER SET 'utf8'")
        print(f"  Banco de dados '{DB_NAME}' criado com sucesso.")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_DB_CREATE_EXISTS:
            print(f"  Banco de dados '{DB_NAME}' já existe.")
        else:
            print(err.msg); exit(1)

def create_tables(cursor):
    cursor.execute(f"USE {DB_NAME}")
    for table_name, table_description in TABLES.items():
        try:
            print(f"  Criando tabela '{table_name}'...", end='')
            cursor.execute(table_description)
            print("OK")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("já existe.")
            else:
                print(err.msg)

def main():
    try:
        cnx = mysql.connector.connect(**DB_CONFIG)
        cursor = cnx.cursor()
        create_database(cursor)
        create_tables(cursor)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("ERRO: Usuário ou senha do MySQL incorretos. Verifique a configuração no topo do script.")
        else:
            print(f"ERRO de Conexão com o MySQL: {err}")
        exit(1)
    else:
        cursor.close(); cnx.close()

if __name__ == "__main__":
    main()
