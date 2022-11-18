__version__ = "1.0.2"
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
# TODO Do i need it?
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

    super().__init__(name, sqlType, opt)
    name:str -> columnName
    sqlType:str -> TEXT, INT, REAL or BLOB
    opt:str -> sqlite column options

    Children classes need overload:
    zip, unzip, __str__
    '''
    def __init__(self, name:str, sqlType, opt:[str, list]=''):
        self.name = name
        if isinstance(opt, str):
            self.opt = [opt]
        else:
            self.opt = opt

        self.type = sqlType
        self.data = None

    # Oveload vvvvvv
    def __str__(self, *args):
        return f'{self.name}={args[0]}'

    def zip(self, *args) -> str:
        self.data = str(args)
        return self

    def unzip(self, *args) -> object:
        return args
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
    '''
    int to INT
    '''
    def __init__(self, name, opt=''):
        super(INTEGER, self).__init__(name=name, opt=opt, sqlType='INTEGER')

    def zip(self, *args) -> Types_SQLite:
        self.data = str(args[0])
        return self

    def unzip(self, *args) -> int:
        return int(args[0])


class TEXT(Types_SQLite):
    '''
    str to TEXT
    '''
    def __init__(self, name, opt=''):
        super(TEXT, self).__init__(name=name, opt=opt, sqlType='TEXT')

    def zip(self, *args:str) -> Types_SQLite:
        self.data = str(args[0])
        return self

    def unzip(self, *args) -> str:
        return f'{args[0]}'


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


    def insert(self,  *args:Types_SQLite, OR='', DEFAULT:bool=False):
        '''
        Write new line in the table with multipe values
        Usage:
        tableName.insert(colunm1.zip(dataToWrite1), ..., columnN.zip(dataToWriteN))

        INSERT [OR <condition>] INTO <tableName> (<column1>, ..., <columnN>)
        VALUES (<inColunm1>, ..., <inColumnN>) | DEFAULT VALUES;

        :param args: Types_SQLite.zip(...), ...,
        :param OR: str -> [OR <condition>]
        :param DEFAULT: bool -> True if [DEFAULT VALUES]
        :return:
        '''

        _text = f'INSERT {OR} INTO {self.tableName} ' \
                f'({", ".join([i.name for i in args])}) ' \
                f'VALUES ({",".join(len(args)*["?"])}) '
        if DEFAULT: _text += 'OR DEFAULT VALUES;'   # Not work

        self.cursor.execute(_text, [i.data for i in args])
        self.base.commit()

        # print(_text)
        return _text, [i.data for i in args]


    def update(self, *args, OR='', WHERE=''):
        '''
        Update the value in the cell
        Usage:
        tableName.update(column1.zip(dataToUpdate1), ..., columnN.zip(dataToUpdateN))

        UPDATE [OR <condition>] [DataBaseName] tableName SET <column1>=<inColunm1>,
         ..., <columnN>=<inColumnN>, [WHERE <condition>];

        :param args: Types_SQLite.zip(...), ...,
        :param OR: str -> [OR <condition>]
        :param WHERE: str -> [WHERE <condition>]
        :return:
        '''

        _text = f'UPDATE {OR} {self.tableName} ' \
                f'SET {",".join([i.name+"=?" for i in args])} '
        if WHERE: _text += f'WHERE {WHERE}'

        self.cursor.execute(_text, [i.data for i in args])
        self.base.commit()

        return _text


    def delete(self, WHERE:str):
        '''
        Delete lines a table that match a condition
        
        DELETE FROM [DatBaseName] tableName WHERE <condition>;

        :param WHERE:str -> WHERE <condition>
        '''
        
        _text = f'DELETE FROM {self.tableName} ' \
                 f'WHERE {WHERE}'

        self.cursor.execute(_text)
        self.base.commit()

        return _text


    def select(self, *args:Types_SQLite, WHERE:str, as_list:bool=False) -> list:
        '''
        Select a columns value from a table
        Usage:
        tableName.select(column1, ..., columnN, WHERE="table1>0")

        SELECT [tableName] <colunm1>, ..., <columnN> | *
        FROM tableName WHERE <condition>


        :param args: Types_SQLite -> columns to return
        :param WHERE: str -> WHERE <condition>
        :param as_list: bool -> if True return values as list
                                if False return as dict
        :return: [[selectedValues1], ..., [selectedValuesN]]
        '''

        _text = f'SELECT {",".join([i.name for i in args])} ' \
                f'FROM {self.tableName} WHERE {WHERE}'

        print(_text)
        self.cursor.execute(_text)
        _result = self.cursor.fetchall()

        if as_list:
            return [self._as_list(*args, _line=i) for i in _result]
        else:
            return [self._as_dict(*args, _line=i) for i in _result]



    def _as_dict(self, *args:Types_SQLite, _line):
        '''Return data as list of dictionaries'''
        return [dict({args[_iter].name : args[_iter].unzip(_val)}) \
                for _iter, _val in enumerate(_line)]


    def _as_list(self, *args:Types_SQLite, _line):
        '''Return data as a list'''
        return [args[_iter].unzip(_val) for _iter, _val in enumerate(_line)]

    """
    MIN, MAX, COUNT, SUM, TOTAL, AWG
    """


    def where(self, *args:Types_SQLite):
        '''

        :param args:
        :return:
        '''
        _text = []
        for i in args:
            _text.append(i.__str__())
        return ' AND '.join(_text)


# ============================================================
if __name__ == '__main__':
    path = Path.cwd()/'sql.db'

    _database = sqlite3.connect(path)
    cursor = _database.cursor()


    link = TEXT(name='link')
    link1 = TEXT(name='link1')
    int1 = INTEGER(name='int1')


    table1 = TableObject('table1', base=_database)
    table1.fillColumns([link, link1, int1])
    table1.createTable()
    print(table1.insert(int1.zip(17), link.zip('asddsa')))
    print(table1.update(link1.zip('17'), WHERE=f'{int1.name}=17'))

    x = table1.select(int1, link1, WHERE=f'int1>0', as_list=True)
    for i in x:
        print(i)

    # print(table1.delete(WHERE=f'{int1.name} > 10 AND {link.name} = "asddsa"'))
    pass
