def build_rtsp_url(ip_address: str, port: str, username: str, password: str) -> str:
    """Constructs the RTSP URL for iCSee camera stream."""
    return  f"rtsp://{username}:{password}@{ip_address}:{port}/user={username}_password={password}_channel=0_stream=0.sdp"


def format_url_path(input_string: str) -> str:
    """Formats the input string to be URL-friendly by replacing whitespace with underscores.
       Accepts only aplhanumeric characters and underscores in the final output.
    """
    # Replace all whitespace with underscores
    formatted = "_".join(input_string.split())
    
    # Remove any characters that are not alphanumeric or underscores
    formatted = ''.join(c for c in formatted if c.isalnum() or c == '_')
    return formatted.lower()
     
def replace_white_spaces(input_string: str) -> str:
    """Replaces all whitespace characters in the input string with underscores."""
    return "_".join(input_string.split())