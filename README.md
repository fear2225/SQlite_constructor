# SQlite sequence constructor  
Python framework for facilitating SQLite database management  
  
---
## Table of contents  


## Dependence
Install pathlib or coment import and FILE lines
```
pip install pathlib
```

## How to use  
See test_main function example
### Connect to database
Start SQLite database connection
```
import sqlite3
Database_connect = sqlite3.connect(path)
```

### Column definition  
Chose python-to-SQLite data method:  
  - TEXT: str -> TEXT  
  - INTEGER: int -> INT  
  - LIST: list -> TEXT(zip list into ','-separated TEXT type)
 ```
 colunm1 = TEXT('columnName1', opt = 'UNIQUE')
 column2 = INTEGER('columnName2')
 '''...'''        '''...'''
 columnN = LIST('columnNameN')
 ```
Or define self data type inhert Types_SQLite class (later)  

### Table definition  
Add table-structure class:
```
tableName = TableObject(name='tableName', base=Database_connect)
tableName.fillColumns(colunm1, ..., columnN) # add columns in table
tableName.createTable() # Create table in database (if not exist)
```

### Relised commands
#### INSERT
Add new row in table
```
tableName.select(column1, ..., columnN")
```
#### UPDATE
Update value in the cell  
[!] use .zip() method
```
tableName.update(column1.zip(dataToUpdate1), ..., columnN.zip(dataToUpdateN))
```
#### DELETE
Delete row, matched the condition
[!] use careful
```
tableName.delete(WHERE=f"{column2}>0)
```
#### SELECT
Select data from table
```
tableName.select(column1, ..., columnN, WHERE=f"{column1}='cat'", as_list=True)
```
return:  
  if as_list=True:  
    [[...], [...], ..., [...]]  
    list of data in sequence it asked   
  alif as_list=False:  
    [[{... : ...}, ..., {... : ...}], ..., [{... : ...}, ..., {... : ...}]]  
    list of pairs {columnName:data} in sequence it asked  
  
## New python-SQLite data type
Class inhertance:
```
class typeName(Types_SQLite):
  def __init__(self, name, opt):
    super().__init__(name=name, sqlType='SQLiteDataType', opt=opt)
    '''
    name:str -> columnName
    sqlType:str -> TEXT, INT, REAL or BLOB
    opt:str -> sqlite column options
    '''
  def zip(dataToZip) -> Types_SQLite:
    self.data = str(dataToZip)   # save data in SQLite analolg type
    return self
  
  def unzip(*args) -> object:
    # do sth to unzip data
    return int(args[0])

```

## Some SQLite
- TEXT <-> str  
- INTEGET <-> int  
- BLOB <-> bytes  
- REAL <-> float
- NULL <-> None
---

## 

