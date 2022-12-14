# SQlite sequence constructor  
Python framework for facilitating SQLite database management  
  
---
## Table of contents  
1) Dependence
2) How to use
   - Colimn definition
   - Table definition
   - Basic commands  
   - Alter table  
   - New python-SQLite data type
3) Some SQLite 

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
  - BOOL: bool -> INT(0|1)  
  - COUNTER: -> PRIMARY KEY AUTOINCREMENT
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

### Basic commands
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
[i] use \*tableName.all() to select all columns
```
tableName.select(column1, ..., columnN, WHERE=f"{column1}='cat'", as_list=True)
```
return:  
  if as_list=True:  
    [[...], [...], ..., [...]]  
    list of data in sequence it asked   
  elif as_list=False:  
    [[{... : ...}, ..., {... : ...}], ..., [{... : ...}, ..., {... : ...}]]  
    list of pairs {columnName:data} in sequence it asked  
#### MIN/MAX
Return unziped min/max column value  
```
tableName.MIN(column)
```  
### AlTER TABLE  
#### ADD COLUMN  
 Add new column  
 ```
 tableName.ADD_COLUMN(column)
 ```
#### DROP COLUMN  
Delete column  
```
tableName.DROP_COLUMN(column)
```
### New python-SQLite data type
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

