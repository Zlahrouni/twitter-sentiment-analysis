"""mysql errors handlers"""
# pylint: disable=R0801

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
    PoolError as MySQLPoolError,
)

def register_mysql_error_handlers(app, format_response):
    """error handlers for mysql database"""

    @app.errorhandler(MySQLInterfaceError)
    def handle_mysql_interface_error(error):
        """MySQLInterfaceError - problèmes de communication avec la base"""
        return format_response.generate_response(
            code=503,
            message=error
        )

    @app.errorhandler(MySQLDatabaseError)
    def handle_mysql_database_error(error):
        """MySQLDatabaseError - erreur générale de base de données"""
        return format_response.generate_response(
            code=500,
            message=error
        )

    @app.errorhandler(MySQLDataError)
    def handle_mysql_data_error(error):
        """MySQLDataError - problèmes avec les données"""
        return format_response.generate_response(
            code=400,
            message=error
        )

    @app.errorhandler(MySQLOperationalError)
    def handle_mysql_operational_error(error):
        """MySQLOperationalError - erreurs liées aux opérations"""
        return format_response.generate_response(
            code=503,
            message=error
        )

    @app.errorhandler(MySQLIntegrityError)
    def handle_mysql_integrity_error(error):
        """MySQLIntegrityError - violation de contraintes d'intégrité"""
        return format_response.generate_response(
            code=409,
            message=error
        )

    @app.errorhandler(MySQLInternalError)
    def handle_mysql_internal_error(error):
        """MySQLInternalError - erreur interne du serveur"""
        return format_response.generate_response(
            code=500,
            message=error
        )

    @app.errorhandler(MySQLProgrammingError)
    def handle_mysql_programming_error(error):
        """MySQLProgrammingError - erreurs de syntaxe ou tables manquantes"""
        return format_response.generate_response(
            code=400,
            message=error
        )

    @app.errorhandler(MySQLNotSupportedError)
    def handle_mysql_not_supported_error(error):
        """MySQLNotSupportedError - fonctionnalité non supportée"""
        return format_response.generate_response(
            code=501,
            message=error
        )

    @app.errorhandler(MySQLPoolError)
    def handle_mysql_pool_error(error):
        """MySQLPoolError - erreur de pool de connexions"""
        return format_response.generate_response(
            code=503,
            message=error
        )

    @app.errorhandler(MySQLError)
    def handle_mysql_error(error):
        """MySQLError - erreur générique MySQL"""
        return format_response.generate_response(
            code=500,
            message=error
        )