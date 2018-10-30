class FileReader:

    def __init__(self, filename):
        self.filename = filename

    def read(self):
        try:
            with open(self.filename, 'r') as f:
                text = f.read()
            return text
        except OSError:
            return ""

""""
Mentors solutions

class FileReader:
    """Класс FileReader помогает читать из файла"""

    def __init__(self, file_name):
        self.file_name = file_name

    def read(self):
        try:
            return open(self.file_name).read()
        except IOError:
            return ""
""""
