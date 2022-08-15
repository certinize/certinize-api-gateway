"""
This type stub file was generated by pyright.
"""

from typing import Any, Dict

class File:
    def __init__(self, request_obj) -> None:
        ...
    
    def upload(self, file, file_name, options) -> Dict:
        """Upload file to server using local image or url
        :param file: either local file path or network file path
        :param file_name: intended file name
        :param options: intended options
        :return: json response from server
        """
        ...
    
    def list(self, options: dict) -> Dict:
        """Returns list files on ImageKit Server
        :param: options dictionary of options
        :return: list of the response
        """
        ...
    
    def details(self, file_identifier: str = ...) -> Dict:
        """returns file detail
        """
        ...
    
    def update_file_details(self, file_id: str, options: dict): # -> dict[str, Unknown | None]:
        """Update detail of a file(like tags, coordinates)
        update details identified by file_id and options,
        which is already uploaded
        """
        ...
    
    def delete(self, file_id: str = ...) -> Dict:
        """Delete file by file_id
        deletes file from imagekit server
        """
        ...
    
    def batch_delete(self, file_ids: list = ...): # -> dict[str, Unknown | None]:
        """Delete bulk files
        Delete files by batch ids
        """
        ...
    
    def purge_cache(self, file_url: str = ...) -> Dict[str, Any]:
        """Use from child class to purge cache
        """
        ...
    
    def get_purge_cache_status(self, cache_request_id: str = ...) -> Dict[str, Any]:
        """Get purge cache status by cache_request_id
        :return: cache_request_id
        """
        ...
    
    def get_metadata(self, file_id: str = ...): # -> dict[str, Unknown | None]:
        """Get metadata by file_id
        """
        ...
    
    def get_metadata_from_remote_url(self, remote_file_url: str): # -> dict[str, Unknown | None]:
        ...
    
    def is_valid_list_options(self, options: Dict[str, Any]) -> bool:
        """Returns if options are valid
        """
        ...
    
    @staticmethod
    def get_valid_list_values(): # -> list[str]:
        """Returns valid options for list files
        """
        ...
    
    @staticmethod
    def validate_upload(options): # -> dict[Unknown, Unknown] | Literal[False]:
        """
        Validates upload value, checks if params are valid,
        changes snake to camel case
        """
        ...
    

