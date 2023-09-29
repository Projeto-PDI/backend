class ProcessFile:
    def getInfo(self, file):
        data = {
            "name": file.filename,
            "type": file.mimetype,
            "length": file.content_length 
        }

        return data