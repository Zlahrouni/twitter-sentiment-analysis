"""Function managing mysql database"""

import mysql.connector
from mysql.connector.errors import (
    Error as MySQLError,
    InterfaceError as MySQLInterfaceError,
    DatabaseError as MySQLDatabaseError,
    DataError as MySQLDataError,
    OperationalError as MySQLOperationalError,
    IntegrityError as MySQLIntegrityError,
    InternalError as MySQLInternalError,
    ProgrammingError as MySQLProgrammingError,
    NotSupportedError as MySQLNotSupportedError,
    PoolError as MySQLPoolError
)
from utils.errors.errors import InternalTypeError
from utils.errors.mysql_errors import (
    MySQLRecordNotFoundError,
    MySQLAuthenticationError,
    MySQLAuthorizationError
)

class MySQLManager:
    """Class to manage MySQL interactions"""
    def __init__(self, host, user, password, database=None):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        """Connect to MySQL database"""
        error_message = "lors de la connection à la base de donnees MySQL."
        if self.database is None:
            raise ValueError("database n'est pas definie")
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor(dictionary=True)
        except Exception as exp:
            handle_mysql_exception(exp=exp, error_message=error_message)
            raise RuntimeError(f"Erreur inaccessible {error_message}.") from exp

    def is_connected(self):
        """Check if connection is active"""
        if self.connection is None:
            return False
        try:
            self.connection.ping(reconnect=True, attempts=1, delay=0)
            return True
        except:
            return False

    def set_database(self, database):
        """Set database name"""
        error_message = "lors de la configuration du nom de la base de donnees MySQL."
        try:
            self.database = database
        except Exception as exp:
            handle_mysql_exception(exp=exp, error_message=error_message)
            raise RuntimeError(f"Erreur inaccessible {error_message}.") from exp

    def find_one(self, query, params=None, disable_404=False):
        """Find single record"""
        error_message = "lors de la requete find_one dans MySQL."
        
        try:
            self.cursor.execute(query, params)
            result = self.cursor.fetchone()
            
            if not result and disable_404 is False:
                message = f"Aucun enregistrement trouve avec la requete {query}"
                raise MySQLRecordNotFoundError(message)
            return result
        except MySQLRecordNotFoundError as exp:
            raise MySQLRecordNotFoundError(exp) from exp
        except Exception as exp:
            handle_mysql_exception(exp=exp, error_message=error_message)
            raise RuntimeError(f"Erreur inaccessible {error_message}.") from exp

    def find_many(self, query, params=None):
        """Find multiple records"""
        error_message = "lors de la requete find_many dans MySQL."
        
        try:
            self.cursor.execute(query, params)
            results = self.cursor.fetchall()
            
            if not results:
                message = f"Aucun enregistrement trouve avec la requete {query}"
                raise MySQLRecordNotFoundError(message)
            return results
        except MySQLRecordNotFoundError as exp:
            raise MySQLRecordNotFoundError(exp) from exp
        except Exception as exp:
            handle_mysql_exception(exp=exp, error_message=error_message)
            raise RuntimeError(f"Erreur inaccessible {error_message}.") from exp

    def insert(self, query, data):
        """Insert record"""
        error_message = "lors de l'insertion dans MySQL."
        
        if not isinstance(data, (dict, tuple)):
            raise InternalTypeError("data doit etre un dictionnaire ou un tuple")

        try:
            self.cursor.execute(query, data)
            self.connection.commit()
            return self.cursor.lastrowid
        except Exception as exp:
            handle_mysql_exception(exp=exp, error_message=error_message)
            raise RuntimeError(f"Erreur inaccessible {error_message}.") from exp

    def update(self, query, data):
        """Update record"""
        error_message = "lors de la mise a jour dans MySQL."
        
        if not isinstance(data, (dict, tuple)):
            raise InternalTypeError("data doit etre un dictionnaire ou un tuple")

        try:
            self.cursor.execute(query, data)
            self.connection.commit()
            return self.cursor.rowcount
        except Exception as exp:
            handle_mysql_exception(exp=exp, error_message=error_message)
            raise RuntimeError(f"Erreur inaccessible {error_message}.") from exp

    def delete_one(self, query, params=None):
        """Delete single record"""
        error_message = "lors de la suppression dans MySQL."
        
        try:
            self.cursor.execute(query, params)
            if self.cursor.rowcount == 0:
                raise MySQLRecordNotFoundError(
                    f"Aucun enregistrement trouve avec la requete {query}"
                )
            self.connection.commit()
        except MySQLRecordNotFoundError as exp:
            raise MySQLRecordNotFoundError(exp) from exp
        except Exception as exp:
            handle_mysql_exception(exp=exp, error_message=error_message)
            raise RuntimeError(f"Erreur inaccessible {error_message}.") from exp

    def count(self, query, params=None):
        """Count records"""
        error_message = "lors de la requete count dans MySQL."
        
        try:
            self.cursor.execute(query, params)
            result = self.cursor.fetchone()
            return result['COUNT(*)'] if result else 0
        except Exception as exp:
            handle_mysql_exception(exp=exp, error_message=error_message)
            raise RuntimeError(f"Erreur inaccessible {error_message}.") from exp

    def distinct(self, column, table, condition=None, params=None):
        """Get distinct values"""
        error_message = "lors de la requete distinct dans MySQL."
        
        query = f"SELECT DISTINCT {column} FROM {table}"
        if condition:
            query += f" WHERE {condition}"
            
        try:
            self.cursor.execute(query, params)
            results = self.cursor.fetchall()
            if not results:
                raise MySQLRecordNotFoundError(f"Aucune valeur trouvée pour {column}")
            return [row[column] for row in results]
        except MySQLRecordNotFoundError as exp:
            raise MySQLRecordNotFoundError(exp) from exp
        except Exception as exp:
            handle_mysql_exception(exp=exp, error_message=error_message)
            raise RuntimeError(f"Erreur inaccessible {error_message}.") from exp

def handle_mysql_exception(exp, error_message=""):
    """Map MySQL errors to custom exceptions"""
    if isinstance(exp, MySQLInterfaceError):
        message = f"Erreur d'interface {error_message} : {exp}"
        raise MySQLInterfaceError(message) from exp
    if isinstance(exp, MySQLOperationalError):
        if 'access denied' in str(exp).lower():
            message = f"Erreur d'authentification {error_message} : {exp}"
            raise MySQLAuthenticationError(message) from exp
        if 'permission denied' in str(exp).lower():
            message = f"Permissions insuffisantes {error_message} : {exp}"
            raise MySQLAuthorizationError(message) from exp
        message = f"Erreur opérationnelle {error_message} : {exp}"
        raise MySQLOperationalError(message) from exp
    if isinstance(exp, MySQLIntegrityError):
        message = f"Erreur d'intégrité {error_message} : {exp}"
        raise MySQLIntegrityError(message) from exp
    if isinstance(exp, MySQLInternalError):
        message = f"Erreur interne {error_message} : {exp}"
        raise MySQLInternalError(message) from exp
    if isinstance(exp, MySQLProgrammingError):
        message = f"Erreur de programmation {error_message} : {exp}"
        raise MySQLProgrammingError(message) from exp
    if isinstance(exp, MySQLNotSupportedError):
        message = f"Fonctionnalité non supportée {error_message} : {exp}"
        raise MySQLNotSupportedError(message) from exp
    if isinstance(exp, MySQLPoolError):
        message = f"Erreur de pool {error_message} : {exp}"
        raise MySQLPoolError(message) from exp
    message = f"Erreur inattendue {error_message} : {exp}"
    raise MySQLError(message) from exp