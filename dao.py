import sqlite3


DB_NAME = 'database/data.db'
CREATE_TABLE = '''
        create table if not exists Terms(
                ID int primary key not null,
                TermName varchar(100) unique not null,
                TermUrl varchar(100) not null,
                TermPic varchar(100),
                Content text not null
        )
'''
INSERT_TERM = "INSERT INTO Terms(ID, TermName, TermUrl, TermPic, Content) VALUES(?, ?, ?, ? , ?);"
SELECT_ALL = "SELECT * from Terms;"
DELETE_TERM = "DELETE FROM Terms WHERE TermName=?;"
TABLE_COL_NAME = ['ID', 'TermName', 'TermUrl', 'TermPic', 'Content']

conn = sqlite3.connect(DB_NAME)
database = conn.cursor()


def create_database_table():
    database.execute(CREATE_TABLE)


def insert_term(no: int, name: str, url: str, pic_url: str, content: str):
    database.execute(INSERT_TERM, (no, name, url, pic_url, content))
    conn.commit()


def show_all_data():
    data = database.execute(SELECT_ALL)
    list_data = list(data)
    for term in list_data:
        print(term)


def delete_term(value: str):
    database.execute(DELETE_TERM, (value,))
    conn.commit()
