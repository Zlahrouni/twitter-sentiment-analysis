"""Errors definition"""

class CallApiError(Exception):
    """Error on api calling."""

class CallApiAuthError(Exception):
    """Error on auth."""

class NoTokenError(Exception):
    """Error token absent"""

class WrongTokenError(Exception):
    """Error wrong token"""

class NoHeaderError(Exception):
    """Error header absent"""

class DatabaseError(Exception):
    """Error on database calling."""

class InternalError(Exception):
    """Error on internal functions."""

class KubernetesConfigError(Exception):
    """Error in Kubernetes API configuration."""

class KubernetesApiError(Exception):
    """Error in Kubernetes API using."""

class KubernetesAuthError(KubernetesApiError):
    """Error in Kubernetes API authentication."""

class KubernetesConnectionError(KubernetesApiError):
    """Error in Kubernetes API connexion."""

class InternalValueError(ValueError):
    """Error in server values."""

class ExternalValueError(ValueError):
    """Error in input values."""

class InternalTypeError(TypeError):
    """Error in server types."""

class ExternalTypeError(TypeError):
    """Error in input types."""

class UnReadyNode(Exception):
    """Node not ready."""

class NotFoundError(Exception):
    """data not found."""

class NotAllowedError(Exception):
    """action not allowed."""
