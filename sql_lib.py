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
1) Remove _text returns in methods      <- Done
2) Add MIN, NAX                         <- Done
3) Add more types                       <- 2 More
4) Add keywords dictionary              <- Done
5) Remove self.data                     <- Done
6) Add more sql function supptort data type
7) ADD/DROP columns                     <- Done
8) ORDER BY ASC/DESC
9) Errors handlers!!!
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

    def IS_NULL(self) -> str:
        return f'{self.name} IS NULL'

    def IS_NOT_NULL(self) -> str:
        return f'{self.name} IS NOT NULL'

    # Oveload vvvvvv
    def __str__(self):
        return f'{self.add()}'

    def zip(self, *args) -> dict:
        return {self.name:str[0]}

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
        return f'"{self.name}" {self.type} {self._add_opt()}'


# ============================================================
class COUNTER(Types_SQLite):
    '''
    AUTOINCRIMENT
    '''
    def __init__(self, name):
        super(COUNTER, self).__init__(name=name, opt=f'{PRIMAK_KEY} {AUTOINCREMENT}', sqlType='INTEGER')

    def zip(self, *args) -> dict:
        return {self.name:None}

    def unzip(self, *args) -> int:
        return int(args[0])


class BOOL(Types_SQLite):
    '''
    Any to bool to INT
    '''
    def __init__(self, name, opt=''):
        super(BOOL, self).__init__(name=name, opt=opt, sqlType='INTEGER')

    def zip(self, *args) -> dict:
        return {self.name:0 if not args[0] else 1}

    def unzip(self, *args) -> bool:
        return bool(args[0])

class INTEGER(Types_SQLite):
    '''
    int to INT
    '''
    def __init__(self, name, opt=''):
        super(INTEGER, self).__init__(name=name, opt=opt, sqlType='INTEGER')

    def zip(self, *args) -> dict:
        return {self.name:int(args[0])}

    def unzip(self, *args) -> int:
        return int(args[0])


class TEXT(Types_SQLite):
    '''
    str to TEXT
    '''
    def __init__(self, name, opt=''):
        super(TEXT, self).__init__(name=name, opt=opt, sqlType='TEXT')

    def zip(self, *args:str) -> dict:
        return {self.name:args[0]}

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

    def zip(self, *args) -> dict:
        return {self.name:str(args[0])}

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
        return {self.name:self.sep.join([str(i) for i in args])}

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
        self.cursor = self.base.cursor()
        self.columns = []   # Add auto fill table


    def all(self) -> list:
        return [i for i in self.columns]


    def fillColumns(self, *args:Types_SQLite) -> None:
        '''
        Add columns in table
        :param columns: list[Types_SQLite]
        :return: None
        '''

        self.columns = [i for i in args]

        return None


    def createTable(self, req=False) -> None:
        '''
        CREATE TABLE IF NOT EXISTS
        tableName (column1, ..., columnN);

        :return: str -> SQLite create table request
        '''

        _text = f'CREATE TABLE IF NOT EXISTS "{self.tableName}" ('
        for i in self.columns:
            _text+= ' ' + i.add() + ','
        _text = _text[:-1] + ');'

        if req: print(_text)
        self.cursor.execute(_text)
        self.base.commit()

        return None


    def insert(self,  *args, OR='', DEFAULT:bool=False, req=False, **kwargs) -> None:
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
        for i in args:
            kwargs|=i

        _text = f'INSERT {OR} INTO "{self.tableName}" ' \
                f'({", ".join([i for i in kwargs.keys()])}) ' \
                f'VALUES ({",".join(len(args)*["?"])}) '
        if DEFAULT: _text += 'OR DEFAULT VALUES;'   # Not work

        if req: print(_text, [i.values() for i in args])
        self.cursor.execute(_text, [i for i in kwargs.values()])
        self.base.commit()

        return None


    def update(self, *args, OR='', WHERE='', req=False, **kwargs) -> None:
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

        if len(args):
            for i in args:
                kwargs|=i

        _text = f'UPDATE {OR} "{self.tableName}" ' \
                f'SET {",".join([i+"=?" for i in kwargs.keys()])} '
        if WHERE: _text += f'WHERE {WHERE}'

        if req: print(_text)
        self.cursor.execute(_text, [i for i in kwargs.values()])
        self.base.commit()

        return None


    def delete(self, WHERE:str, req=False) -> None:
        '''
        Delete lines a table that match a condition

        DELETE FROM [DatBaseName] tableName WHERE <condition>;

        :param WHERE:str -> WHERE <condition>
        '''
        
        _text = f'DELETE FROM "{self.tableName}" ' \
                 f'WHERE {WHERE}'

        if req: print(_text)
        self.cursor.execute(_text)
        self.base.commit()

        return None


    def select(self, *args:Types_SQLite, WHERE:str='', as_list:bool=False, req=False) -> list:
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
                f'FROM "{self.tableName}" '
        if WHERE: _text += f'WHERE {WHERE}'

        if req: print(_text)
        self.cursor.execute(_text)
        _result = self.cursor.fetchall()

        return [self._as_list(*args, _line=i) for i in _result] if as_list \
                else [self._as_dict(*args, _line=i) for i in _result]


    # ALTER TABLE
    def ADD_COLUMN(self, column:Types_SQLite, req=False) -> None:
        '''
        Add new column

        ALTER TABLE <tableName> ADD COLUMN <columnName> <type>

        :param column: Types_SQLite
        :return: None
        '''

        _text = f'ALTER TABLE {self.tableName} ' \
                f'ADD COLUMN {column.add()}'

        if req: print(_text)
        self.cursor.execute(_text)
        self.base.commit()

        self.columns.append(column)

        return None


    def DROP_COLUMN(self, column:Types_SQLite, req=False) -> None:
        '''
        Delete column

        ALTER TABLE <tableName> DROP COLUMN <columnName>

        :param column: str -> columnName
        :return: None
        '''

        _text = f'ALTER TABLE {self.tableName} ' \
                f'DROP COLUMN {column.name}'

        if req: print(_text)
        self.cursor.execute(_text)
        self.base.commit()

        if column in self.columns:
            self.columns.pop(column)

        return None


    # One resulr funktions
    def MAX(self, column:Types_SQLite):
        '''
        Return max value

        SELECT MAX(<column>) FROM tableName

        :param column: Types_SQLite
        :return: unzip(MAX(column))
        '''
        _text = f"SELECT MAX ({column.name}) FROM {self.tableName}"

        self.cursor.execute(_text)
        _result = self.cursor.fetchone()

        return column.unzip(_result[0])


    def MIN(self, column:Types_SQLite):
        '''
        Return min value

        SELECT MIN(<column>) FROM tableName

        :param column: Types_SQLite
        :return: unzip(MIN(column))
        '''
        _text = f"SELECT MIN ({column.name}) FROM {self.tableName}"

        self.cursor.execute(_text)
        _result = self.cursor.fetchone()

        return column.unzip(_result[0])

    #
    # def AWG(self, column:Types_SQLite):
    #     '''
    #     Return AWG value
    #
    #     SELECT AWG(<column>) FROM tableName
    #
    #     :param column: Types_SQLite
    #     :return: unzip(AWG(column))
    #     '''
    #     _text = f"SELECT AWG ({column.name}) FROM {self.tableName}"
    #
    #     self.cursor.execute(_text)
    #     _result = self.cursor.fetchone()
    #
    #     return column.unzip(_result[0])


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
                            size.zip(_temp[2]))


    for i in imaglink.select(*imaglink.all()):
        print(i)

    newColumn1 = TEXT('test1')
    newColumn2 = TEXT('test2')

    imaglink.ADD_COLUMN(newColumn1, req=True)
    print(imaglink.columns)
    imaglink.ADD_COLUMN(newColumn2, req=True)
    print(imaglink.columns)

    imaglink.DROP_COLUMN(newColumn1, req=True)
    print(imaglink.columns)

    print(ENDL, imaglink.MAX(url))
    print(ENDL, imaglink.MIN(url))

    # end
    pass


# ============================================================
if __name__ == '__main__':
    test_main()


    pass