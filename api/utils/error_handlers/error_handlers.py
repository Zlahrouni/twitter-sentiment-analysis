"""error handlers"""
# pylint: disable=R0801

from utils.errors.errors import (
    CallApiError,
    CallApiAuthError,
    NoTokenError,
    WrongTokenError,
    NoHeaderError,
    DatabaseError,
    InternalError,
    KubernetesConfigError,
    KubernetesApiError,
    KubernetesAuthError,
    KubernetesConnectionError,
    InternalValueError,
    ExternalValueError,
    InternalTypeError,
    ExternalTypeError,
    UnReadyNode,
    NotFoundError,
    NotAllowedError
)

def register_error_handlers(app, format_response):  # pylint: disable=too-many-locals
    """error handlers for api"""

    @app.errorhandler(CallApiError)
    def handle_call_api_error(error):
        """CallApiError"""
        return format_response.generate_response(
            code=500,
            message=error
        )

    @app.errorhandler(CallApiAuthError)
    def handle_call_api_auth_error(error):
        """CallApiAuthError"""
        return format_response.generate_response(
            code=403,
            message=error
        )

    @app.errorhandler(NoTokenError)
    def no_token_error(error):
        """NoTokenError"""
        return format_response.generate_response(
            code=401,
            message=error
        )

    @app.errorhandler(WrongTokenError)
    def wrong_token_error(error):
        """WrongTokenError"""
        return format_response.generate_response(
            code=401,
            message=error
        )

    @app.errorhandler(NoHeaderError)
    def no_header_error(error):
        """NoHeaderError"""
        return format_response.generate_response(
            code=401,
            message=error
        )

    @app.errorhandler(DatabaseError)
    def handle_database_error(error):
        """DatabaseError"""
        return format_response.generate_response(
            code=500,
            message=error
        )

    @app.errorhandler(InternalError)
    def handle_internal_error(error):
        """InternalError"""
        return format_response.generate_response(
            code=500,
            message=error
        )

    @app.errorhandler(KubernetesConfigError)
    def handle_kubernetes_config_error(error):
        """KubernetesConfigError"""
        return format_response.generate_response(
            code=500,
            message=error
        )

    @app.errorhandler(KubernetesApiError)
    def handle_kubernetes_api_error(error):
        """KubernetesApiError"""
        return format_response.generate_response(
            code=500,
            message=error
        )

    @app.errorhandler(KubernetesAuthError)
    def handle_kubernetes_auth_error(error):
        """KubernetesAuthError"""
        return format_response.generate_response(
            code=401,
            message=error
        )

    @app.errorhandler(KubernetesConnectionError)
    def handle_kubernetes_connection_error(error):
        """KubernetesConnectionError"""
        return format_response.generate_response(
            code=502,
            message=error
        )

    @app.errorhandler(ValueError)
    def handle_value_error(error):
        """ValueError"""
        return format_response.generate_response(
            code=500,
            message=error
        )

    @app.errorhandler(InternalValueError)
    def handle_internal_value_error(error):
        """InternalValueError"""
        return format_response.generate_response(
            code=500,
            message=error
        )
    @app.errorhandler(ExternalValueError)
    def handle_external_value_error(error):
        """ExternalValueError"""
        return format_response.generate_response(
            code=400,
            message=error
        )

    @app.errorhandler(TimeoutError)
    def handle_timeout_error(error):
        """TimeoutError"""
        return format_response.generate_response(
            code=504,
            message=error
        )

    @app.errorhandler(TypeError)
    def handle_type_error(error):
        """TypeError"""
        return format_response.generate_response(
            code=400,
            message=error
        )

    @app.errorhandler(KeyError)
    def handle_key_error(error):
        """KeyError"""
        return format_response.generate_response(
            code=500,
            message=error
        )

    @app.errorhandler(InternalTypeError)
    def handle_internal_type_error(error):
        """InternalTypeError"""
        return format_response.generate_response(
            code=500,
            message=error
        )

    @app.errorhandler(ExternalTypeError)
    def handle_external_type_error(error):
        """ExternalTypeError"""
        return format_response.generate_response(
            code=400,
            message=error
        )

    @app.errorhandler(UnReadyNode)
    def handle_unready_node(error):
        """UnReadyNode"""
        return format_response.generate_response(
            code=204,
            message=error
        )

    @app.errorhandler(NotFoundError)
    def handle_not_found_error(error):
        """NotFoundError"""
        return format_response.generate_response(
            code=404,
            message=error
        )

    @app.errorhandler(NotAllowedError)
    def handle_not_allowed_error(error):
        """NotAllowedError"""
        return format_response.generate_response(
            code=403,
            message=error
        )
