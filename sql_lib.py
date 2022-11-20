__version__ = "1.1.0"
__author__ = "https://github.com/fear2225"

import requests

'''
    Python-SQLite framwork

[*] In PyCharm comment trouble :c
[!] Not fully tested :c
'''

# TODO List
"""
1) Remove _text returns in methods
2) Add MIN, NAX ... etc
3) Add more types
4) Add keywords dictionary
5) Remove self.data
6) Add more sql function supptort data type
"""


# Internal
import sqlite3

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
    def __str__(self):
        return f'{self.add()}'

    def zip(self, *args) -> object:
        self.data = str(args[0])
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


# ============================================================
class COUNTER(Types_SQLite):
    '''
    AUTOINCRIMENT
    '''
    def __init__(self, name):
        super(COUNTER, self).__init__(name=name, opt=f'{PRIMAK_KEY} {AUTOINCREMENT}', sqlType='INTEGER')
        self.data = None

    def zip(self, *args) -> Types_SQLite:
        return self

    def unzip(self, *args) -> int:
        return int(args[0])


class BOOL(Types_SQLite):
    '''
    Any to bool to INT
    '''
    def __init__(self, name, opt=''):
        super(BOOL, self).__init__(name=name, opt=opt, sqlType='INTEGER')

    def zip(self, *args) -> Types_SQLite:
        if not args[0]:
            self.data = 0
        else:
            self.data = 1
        return self

    def unzip(self, *args) -> bool:
        return bool(args[0])

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


# todo Path to TEXT
class FILE(Types_SQLite):
    '''
    file path to TEXT, unzip - open file
    '''
    def __init__(self, name, root:Path, opt=''):
        super(FILE, self).__init__(name=name, opt=opt, sqlType='TEXT')
        self.root = root

    def zip(self, *args) -> Types_SQLite:
        self.data = str(args[0])
        return self

    def unzip(self, *args) -> Path:
        return args[0]

    @staticmethod
    def nameGen(start:int=1):
        while True:
            yield str(start)
            start+=1


class LIST(Types_SQLite):
    '''
    list to TEXT, zip separated by sep="," (default)
    '''
    def __init__(self, name, opt='', sep:str=','):
        super(LIST, self).__init__(name=name, opt=opt, sqlType='TEXT')
        self.sep = sep

    def zip(self, *args) -> Types_SQLite:
        self.data = self.sep.join([str(i) for i in args])
        return self

    def unzip(self, *args:str) -> list:
        return args[0].split(sep=self.sep)


# ============================================================
# TODO maybe one day...
# class Functions_SQLite(Types_SQLite):
#     def __init__(self):
#         self.name = ''
#
#     def MAX(self, column_:Types_SQLite):
#         self.name = f'MAX ({column_.name})'
#         return self


# ============================================================
class TableObject():
    '''
    Common Usage:
    # Connect
    DataBase_connect = sqlite3.connect(path)

    # Table creation
    TableName = TableObject(name=tableName, base=DataBase_connect)
    columnName1 = TEXT()
        ...        ...
    columnNameN = INTEGER()
    TableName.fillColumns(columnName1.add(), ..., columnNameN.add())
    TableName.createTable()
    
    # Use methods
    TableName.insert(columnName1, ..., colinmNameN)
    tableData = TableName.select(colunmName1, ..., columnNameN)
    TableName.delete(*TableName.all())
    
    '''

    def __init__(self, name:str, base:sqlite3.Connection):
        self.tableName = name
        self.base = base
        print(self.base)
        self.cursor = self.base.cursor()
        self.columns = []   # Add auto fill table


    def all(self):
        return [i for i in self.columns]


    def fillColumns(self, *args:Types_SQLite) -> None:
        '''
        Add columns in table
        :param columns: list[Types_SQLite]
        :return: None
        '''

        self.columns = [i for i in args]


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


    def select(self, *args:Types_SQLite, WHERE:str='', as_list:bool=False) -> list:
        '''
        Select a columns value from a table
        For all select (*) use: *tableName.all()
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
                f'FROM {self.tableName} '
        if WHERE: _text += f'WHERE {WHERE}'

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


# ============================================================


# TODO I don`t know how it works, but may be one day...
"""MIN, MAX, COUNT, SUM, TOTAL, AWG"""

def defineFunk_name(funk):
    '''Funcktion mane become variable'''
    def target(column):
        return funk(funk.__name__, column)
    return target

@defineFunk_name
def MAX(name, column:Types_SQLite) -> str: return f' {name} ({column.name}) '


def where(self, *args):
    '''
    Method connect different conditions with " AND "

    :param args: str -> <conditions> to connect
    :return: str -> <condition1> AND ... AND <conditionN>
    '''
    _text = []
    for i in args:
        _text.append(i.__str__())
    return ' AND '.join(_text)


# ============================================================
def test_main():
    '''
    Download and save in database 3 cat pictures
    '''

    path = Path.cwd()/'sql.db'

    _database = sqlite3.connect(path)
    cursor = _database.cursor()

    # test
    imgNameGen = FILE.nameGen(0)
    gen_next = imgNameGen.__next__

    count = COUNTER(name='count')
    url = TEXT(name='url')
    image = FILE(name='image', root=Path.cwd())
    size = INTEGER(name='size')

    imaglink = TableObject('imaglink', base=_database)
    imaglink.fillColumns(count, url, image, size)
    imaglink.createTable()

    testURL = ["https://img2.joyreactor.cc/pics/post/%D0%BA%D0%BE%D1%82%D1%8D-7698621.jpeg",
                "https://img2.joyreactor.cc/pics/post/%D0%BA%D0%BE%D1%82%D1%8D-7698620.png",
               "https://img2.joyreactor.cc/pics/post/%D0%BA%D0%BE%D1%82%D1%8D-7698619.jpeg"]
    import requests
    for i in range(3):
        req = requests.get(testURL[i])
        _temp = [testURL[i], image.root/(gen_next()+'.jpg')]
        print(_temp)
        with open(_temp[1], 'wb') as f:
            f.write(req.content)
            _temp.append(
                _temp[1].stat().st_size
            )

            imaglink.insert(count.zip(),
                            url.zip(_temp[0]),
                            image.zip(_temp[1]),
                            size.zip(_temp[2]))

    for i in imaglink.select(*imaglink.all()):
        print(i)

    # end
    pass


# ============================================================
if __name__ == '__main__':
    test_main()
    pass