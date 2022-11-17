__version__ = "1.0.1"
__author__ = "https://github.com/fear2225"
'''
[!] In PyCharm comment trouble :c
[!] One DataBase one connection method
'''


# Internal
import sqlite3
import types

from pathlib import Path

# External

# Consts
ENDL = '\n' + '*' * 80 + '\n'


# ============================================================
# REAL = 'REAL' todo maby i need it later (float)
# BLOB = 'BLOB' todo make pickle data type


NULL = 'NULL'

PRIMAK_KEY = 'PRIMARY KEY'
UNIQUE = 'UNIQUE'
NOT_NULL = 'NOT NULL'

def CHECK(text): return f'CHECK {text}'
def DEFAULT(text): return f'DEFAULT {text}'
AUTOINCREMENT = 'AUTOINCREMENT'

# ============================================================
def tryExcept(toExec):
    def _targetFunc(*args, **kwargs):
        try:
            targetReturn = toExec(*args, **kwargs)
            return targetReturn
        except:
            print(f'[!] Error in <{toExec.__name__}>!')
            return None

    return _targetFunc

# TODO comments
class Types_SQLite:
    '''
    Parent class for SQLite data types
    Children classes need overload:
    zip, unzip, __str__
    '''
    def __init__(self, name:str, opt:[str, list]=''):
        self.name = name
        if isinstance(opt, str):
            self.opt = [opt]
        else:
            self.opt = opt

        self.type = 'None'
        self.data:bytes = None

    # Oveload vvvvvv
    def __str__(self):
        return self.data.decode()

    def zip(self, arg:str) -> None:
        self.data = arg.encode()

    def unzip(self):
        return self.data
    # Overload ^^^^^^

    def addOpt(self, *args):
        for i in args:
            self.opt.append(i)

    # Create table methods
    def _add_opt(self) -> str:
        if not self.opt:
            return ''
        return ' '.join([i for i in self.opt])

    def add(self) -> str:
        return f'{self.name} {self.type} {self._add_opt()},'


class INTEGER(Types_SQLite):
    def __init__(self, name, opt=''):
        super(INTEGER, self).__init__(name, opt)
        self.type = 'INTEGER'

    def __str__(self):
        return f'{self.data}'

    def zip(self, arg) -> None:
        self.data = int(arg)

    def unzip(self):
        return self.data


class TEXT(Types_SQLite):
    def __init__(self, name, opt=''):
        super(TEXT, self).__init__(name, opt)
        self.type = 'TEXT'

    def __str__(self):
        return self.data

    def zip(self, arg:str) -> None:
        self.data = str(self.data)

    def unzip(self):
        return self.data


class TableObject():
    '''
    Common Usage:
    # Connect
    DataBase_connect = sqlite3.connect(path)
    DataBase_cursor = DataBase_connect.cursor()
    # Table creation
    TableName = TableObject(name=tableName, cursor=DataBase_cursor)
    TableName.fillColumns(column1:Types_SQLite, ..., columnN:Types_SQLite)
    TableName.createTable()

    '''

    def __init__(self, name:str, base:sqlite3.Connection):
        self.tableName = name
        self.base = base
        print(self.base)
        self.cursor = self.base.cursor()
        self.columns = []   # Add auto fill table



    def fillColumns(self, columns:list[Types_SQLite]) -> None:
        '''
        Add columns in table
        :param columns: list[Types_SQLite]
        :return: None
        '''
        self.columns = columns


    def createTable(self):
        '''
        CREATE TABLE IF NOT EXISTS
        tableName (column1, ..., columnN);

        :return: str -> SQLite create table request
        '''
        _text = f'CREATE TABLE IF NOT EXISTS {self.tableName} ('
        for i in self.columns:
            _text+= ' ' + i.add()
        _text = _text[:-1] + ');'
        print(_text)    # todo remove

        self.cursor.execute(_text)
        self.base.commit()
        return _text


    def insert(self,  *args, OR='', DEFAULT:bool=False, **kwargs):
        '''
        Write new line in table with args and or kwargs walues

        INSERT [OR <if>] INTO <tableName> (<column1>, ..., <columnN>)
        VALUES (<inColunm1>, ..., <inColumnN>) | DEFAULT VALUES;


        :param args: clolumnName1, toColumn1, ..., ..., columnNameN, toColumnN
        :param OR: str -> [OR <condition>]
        :param DEFAULT: bool -> True if [DEFAULT VALUES]
        :param kwargs: {columnName1:toColumn1, ..., columnNameN:toColumnN}
        :return:
        '''

        # args to kwargs
        kwargs = {**kwargs, **{args[i]:args[i+1] for i in range(len(args)) if not i%2}}

        _key, _val = [], []
        for k, v in kwargs.items():
            _key.append(k)
            _val.append(v)

        _text = f'INSERT {OR} INTO {self.tableName} ' \
                f'({", ".join(_key)}) ' \
                f'VALUES ({",".join(len(_key)*["?"])}) '
        if DEFAULT: _text += 'OR DEFAULT VALUES;'   # Not work

        self.cursor.execute(_text, _val)
        self.base.commit()

        # print(_text)
        return _key, _val


    def update(self, *args, OR='', WHERE='', **kwargs):
        '''
        Update columns in table with args or kwargs

        UPDATE [OR <if>] [DataBaseName] tableName SET <column1>=<inColunm1>,
         ..., <columnN>=<inColumnN>, [WHERE <if>];

        :param args: clolumnName1, toColumn1, ..., ..., columnNameN, toColumnN
        :param OR: str -> [OR <condition>]
        :param WHERE: str -> [WHERE <condition>]
        :param kwargs: {columnName1:toColumn1, ..., columnNameN:toColumnN}
        :return:
        '''

        # args to kwargs
        kwargs = {**kwargs, **{args[i]: args[i + 1] for i in range(len(args)) if not i % 2}}

        _key, _val = [], []
        for k, v in kwargs.items():
            _key.append(k)
            _val.append(v)

        _text = f'UPDATE {OR} {self.tableName} ' \
                f'SET {",".join([i+"=?" for i in _key])} '
        if WHERE: _text += f'WHERE {WHERE}'

        self.cursor.execute(_text, _val)
        self.base.commit()

        # print(_text)
        return _key, _val


    """
    DELETE FROM [DatBaseName] tableName
    [WHERE <if>];
    """

    '''
    SELECT [tableName] <colunm1>, ..., <columnN> | *
    FROM tableName WHERE <if>
    '''

    """
    MIN, MAX, COUNT, SUM, TOTAL, AWG
    """



# ============================================================
if __name__ == '__main__':
    path = Path.cwd()/'sql.db'
    #
    # x = DataBase(path=path)
    # print(x.execAndCommit())

    _database = sqlite3.connect(path)
    cursor = _database.cursor()


    link = TEXT(name='link')
    link1 = TEXT(name='link1')
    int1 = INTEGER(name='int1')

    # int1.addOpt(UNIQUE, PRIMAK_KEY, DEFAULT(f'10'))

    table1 = TableObject('table1', base=_database)
    table1.fillColumns([link, link1, int1])
    table1.createTable()
    print(table1.insert(int1.name, 124, link.name, 'niece!', link1.name, 'qwenperfect!'))
    table1.update(link.name, 'it`s working!', WHERE=f'{int1.name} == 124')

    pass
