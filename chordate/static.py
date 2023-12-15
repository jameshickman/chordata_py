import os
import mimetypes
import time
from email.utils import formatdate
from email.utils import parsedate
from chordate.output_stream import CHUNK_SIZE, file_buffer


def static_file_exists(working_directory: str, pathname: str, tenant: str):
    if pathname == '/':
        return False
    path_parts = pathname.split('/')
    application = path_parts[1]
    if len(path_parts) > 2:
        filename = str(os.path.sep).join(path_parts[2:])
        physical_path_name = os.path.join(working_directory, "apps", application, "static", filename)
        if os.path.exists(physical_path_name):
            return physical_path_name
    filename = str(os.path.sep).join(path_parts[1:])
    tenant_local_physical_name = os.path.join(working_directory, "static", tenant, filename)
    if os.path.exists(tenant_local_physical_name):
        return tenant_local_physical_name
    physical_path_name = os.path.join(working_directory, "static", "_global", filename)
    if os.path.exists(physical_path_name):
        return physical_path_name
    else:
        return False


def serve_static(environ, start_response, physical_file: str):
    r = [''.encode()]
    file_ext = physical_file.split(".")[-1]
    file_mime = mimetypes.guess_type(physical_file)
    if file_ext.lower() == "css":
        file_mime = "text/css"
    if file_ext.lower() == "js":
        file_mime = "text/javascript"
    if file_ext.lower() == "json":
        file_mime = "application/json"
    file_mtime = int(os.path.getmtime(physical_file))
    file_size = os.path.getsize(physical_file)
    cc_header = environ.get('HTTP_IF_MODIFIED_SINCE')
    if cc_header:
        cached_file_ts = int(time.mktime(parsedate(cc_header)))
    else:
        cached_file_ts = 0
    in_cache = False
    if cc_header:
        if file_mtime == cached_file_ts:
            in_cache = True
    mtime_datetime = formatdate(timeval=file_mtime, localtime=False, usegmt=True)
    headers = [
        ('Last-Modified', str(mtime_datetime)),
        ('Content-Type', str(file_mime)),
        ('Content-Length', str(file_size))
    ]
    if in_cache:
        start_response("304 Not Modified", headers)
        return []
    else:
        """
        Load and return the content of the file
        """
        start_response("200 OK", headers)
        fp = open(physical_file, 'rb')
    return file_buffer(fp, CHUNK_SIZE)
