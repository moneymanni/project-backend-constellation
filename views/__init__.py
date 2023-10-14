from .index_view import create_endpoint
from .auth_view import create_auth_endpoint
from .user_view import create_user_endpoint
from .note_view import create_note_endpoint
from .page_view import create_page_endpoint
from .link_view import create_link_endpoint
from .tag_view import create_tag_endpoint
from .visualization_view import create_visualization_endpoint
from .recommend_view import create_recommend_endpoint

__all__ = [
    "create_endpoint",
    "create_auth_endpoint",
    "create_user_endpoint",
    "create_note_endpoint",
    "create_page_endpoint",
    "create_link_endpoint",
    "create_tag_endpoint",
    "create_visualization_endpoint",
    "create_recommend_endpoint"
]