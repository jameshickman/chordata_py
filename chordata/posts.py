import cgi
import json


class POSTdata:
    def __init__(self, environ):
        """
        Set a flag indicating that the request is a POST.
        Set a flag if its a JSON type payload.
        """
        self.e = environ
        if environ['REQUEST_METHOD'].upper() != 'POST':
            self.isReqPOST = False
            self.isJSONpost = False
        else:
            self.isReqPOST = True
            if environ.get('CONTENT_TYPE', '').lower() == 'application/json' \
                    or environ.get('CONTENT_TYPE', '').lower() == 'text/json':
                self.isJSONpost = True
            else:
                self.isJSONpost = False
        return
    
    def isPost(self):
        return self.isReqPOST
    
    def getValues(self):            # Parse the POST data using CGI Lib
        """
        Return the POST data as a dictionary.
        For file uploads the 'upload' flag is true and the
        open file-handle provided. 
        """
        v = {}
        inp = self.e['wsgi.input']
        fs = cgi.FieldStorage(fp=inp, environ=self.e, keep_blank_values=1)
        try:
            for field in fs.keys():
                fi = {}
                field_item = fs[field]
                if type(field_item) is list:
                    fi['upload'] = False
                    fi['value'] = fs[field]
                elif field_item.filename:
                    fi['upload'] = True
                    fi['content'] = field_item.file.read()
                    fi['name'] = field_item.filename
                else:
                    fi['upload'] = False
                    fi['value'] = fs[field].value
                v[field] = fi
        except Exception as e:
            pass
        return v

    def isJSON(self):
        return self.isJSONpost
    
    def getJSON(self):
        """
        Retrieve the raw POST data and try to parse it as JSON.
        Return the data structure or False on failure.
        """
        body = ''
        try:
            length = int(self.e.get('CONTENT_LENGTH', '0'))
        except ValueError:
            length = 0
        if length != 0:
            body = self.e['wsgi.input'].read(length).decode(encoding="utf-8")
        try:
            payload = json.loads(body)
        except Exception as e:
            return False
        return payload
