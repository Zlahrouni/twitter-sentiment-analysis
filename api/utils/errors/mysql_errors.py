"""MySQL errors definition"""

from mysql.connector.errors import OperationalError as MySQLOperationalError

class MySQLRecordNotFoundError(Exception):
    """Record not found in MySQL"""

class MySQLAuthenticationError(MySQLOperationalError):
    """Error on authentication in MySQL."""

class MySQLAuthorizationError(MySQLOperationalError):
    """Error on authorization in MySQL."""