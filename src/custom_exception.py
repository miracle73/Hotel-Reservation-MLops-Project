import sys
import traceback

class CustomException(Exception):
    """
    Custom exception class to handle detailed error reporting.
    This class captures the exception details and provides formatted error messages.
    """
    def __init__(self, error_message, error_detail=None):
        super().__init__(error_message)
        
        if error_detail is not None:
            # Handle the exception object case
            if isinstance(error_detail, Exception):
                self.error_message = self._format_exception_message(error_message, error_detail)
            # Handle the sys module case (original usage pattern)
            elif error_detail is sys:
                self.error_message = self._get_sys_detailed_error_message(error_message)
            # Handle string or other error details
            else:
                self.error_message = f"{error_message}: {str(error_detail)}"
        else:
            self.error_message = error_message
    
    def _format_exception_message(self, error_message, exception):
        """Format error message with exception details."""
        tb_str = ''.join(traceback.format_exception(
            type(exception), 
            exception, 
            exception.__traceback__
        ))
        return f"{error_message}\n\nException details:\n{tb_str}"
    
    def _get_sys_detailed_error_message(self, error_message):
        """Get detailed error message using sys.exc_info()."""
        exc_type, exc_obj, exc_tb = sys.exc_info()
        if exc_tb:
            file_name = exc_tb.tb_frame.f_code.co_filename
            line_number = exc_tb.tb_lineno
            return f"Error in {file_name}, line {line_number}: {error_message}"
        return error_message
    
    def __str__(self):
        return self.error_message

