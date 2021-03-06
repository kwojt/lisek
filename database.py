# Database for LMA
# by kwojt (c)
##################

import pickle


class DBColumnError(Exception):
    """
    Exception for methods that tried to use not-existing column.
    """
    def __init__(self, columnName):
        self.columnName = columnName


class DBRecordError(Exception):
    """
    Exception passed if function tried to modify record 0.
    """
    def __init__(self, record):
        self.record = record


class DBError(Exception):
    """
    General exception passed by module.
    """
    pass


class Table:
    """
    Class used to create database-like tables.
    """

    def __init__(self):
        self.table = []
        self.table.append({'id': None})  # Record 0 is for checking keys etc
        self._lastID = 0

    def addColumn(self, name, value=None):
        """
        Adds column with a given name. All records get default
        vaule None in this column if not given any other value.

        Args:
        -----
        string: name -- name of a new column
        void: value -- a value for new column, given to all records

        Raises:
        -------
        DBColumnError -- if column with a given name already exists
        """
        if name in self.table[0]:
            raise DBColumnError(name)
        for record in self.table:
            record[name] = value

    def renameColumn(self, name, newName):
        """
        Renames existing column.

        Args:
        -----
        string: name -- name of existing column
        string: newName -- new name for column

        Raises:
        -------
        DBColumnError -- if column with given name does not exist
        or tried to edit id column
        """
        if name not in self.table[0] or name == 'id':
            raise DBColumnError(name)
        for record in self.table:
            record[newName] = record.pop(name, None)

    def deleteColumn(self, name):
        """
        Remove column with a given name.

        Args:
        -----
        string: name -- name of a column to be deleted

        Raises:
        -------
        DBColumnError -- if column does not exist
        """
        if name not in self.table[0]:
            raise DBColumnError(name)
        for record in self.table:
            record.pop(name, None)
        pass

    def returnColumn(self, name):
        """
        Returns column with a given name.

        Args:
        -----
        string: name -- name of a column

        Returns:
        --------
        List with a values in a certain column.

        Raises:
        -------
        DBError if there isn't column with a given name in table.
        """
        if name not in self.table[0]:
            raise DBError()
        values = []
        iterRecords = iter(self.table)
        next(iterRecords)
        for element in iterRecords:
            values.append(element[name])
        return values

    def addRecord(self, *fields):
        """
        Puts new record in database. Fills not given columns
        with None.

        Args:
        -----
        list: *fields -- lists with column names and their values

            example:
            newRecord(['name', 'John'], ['surname', 'Kowalsky'])

        Raises:
        -------
        DBColumnError -- if wrong column name was given. \
        Also if tried to maually edit 'id' column.

        Returns:
        --------
        Returns 'id' of a new record.
        """
        if not fields:
            return
        for field in fields:
            if field[0] not in self.table[0] or field[0] == 'id':
                raise DBColumnError(field[0])
        self._lastID = self._lastID + 1
        self.table.append({})
        self.table[-1]['id'] = self._lastID
        for field in fields:
            self.table[-1][field[0]] = field[1]
        return self._lastID

    def modifyRecord(self, key, *fields):
        """
        Modifies records with given key.
        """
        for record in self.table:
            if record[key[0]] == key[1]:
                for field in fields:
                    record[field[0]] = field[1]

    def clearDuplicates(self, key):
        """
        DO NOT USE!!!
        NOT READY, GIVES SHIT!!!
        Remove duplicates by searching in certain 'key' column.
        May take a while

        Args:
        -----
        string: key -- column name
        """
        if key not in self.table[0]:
            raise DBError()
        # TODO make it better...
        for record in self.table:
            for checked in self.table:
                if record[key] == checked[key]:
                    del checked

    def deleteRecord(self, id):
        """
        Removes record with given ID.
        I have no idea how to known what record's ID is, lol
        You can't delete record 0 though.

        Args:
        -----
        int: id -- id of a record to delete

        Raises:
        -------
        DBRecordError with 'record' value 0 if tried to modify key
        record or id if tried to delete nonexistent record.
        """
        if id == 0:
            raise DBRecordError(0)
        try:
            del self.table[id]
        except IndexError:
            raise DBRecordError(id)

    def pickleTable(self, file=None):
        """
        Function pickes a table.

        Args:
        -----
        file: [file] -- file object to picke to.

        Returns:
        --------
        String with pickle object if no file was given.
        """
        if file:
            pickle.dump(self.table, file)
        else:
            return pickle.dumps(self.table)
        pass

    def mergeTable(self, table, ifForce=False):
        """
        Merges given table into self.
        Table must be an instance of Table.table.
        Pushes None values if certain columns were not filled.

        Args:
        -----
        Table: table -- table to merge
        bool: ifForce -- when set to true, adds new columns, so
        self.table fits given table

        Raises:
        -------
        DBError -- if error occured, for example if tried to merge
        table with unknown columns without ifForce = true.
        """
        # Checking columns compatilibity
        for column in table[0].keys():
            if column not in self.table[0]:
                if ifForce is True:
                    self.addColumn(column)
                else:
                    raise DBError()
        # Merging
        iterRecords = iter(table)
        next(iterRecords)
        for record in iterRecords:
            self._lastID += 1
            self.table.append(record)
            self.table[-1]['id'] = self._lastID
