from fastapi import HTTPException as FastAPIHTTPException
from typing import Any, Dict, Optional

class HTTPException(FastAPIHTTPException):
    """
    Custom HTTPException that uses 'message' instead of 'detail'
    for consistent API responses across the entire application.
    """
    def __init__(
        self,
        status_code: int,
        message: str,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        # Call the parent with 'detail' parameter but use our 'message'
        super().__init__(status_code=status_code, detail=message, headers=headers)
        
    @property
    def message(self) -> str:
        """Alias for detail to maintain backwards compatibility"""
        return self.detail
        
    @message.setter 
    def message(self, value: str) -> None:
        """Allow setting message which updates detail"""
        self.detail = value