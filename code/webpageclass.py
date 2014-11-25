# Class to store and write webpages
class webpage:
    def __init__(self, name, title, content):
        self.content = content
        self.title = title
        self.name = name
        self.html = ""
        
    # Writes page to file
    def write(self, directory, overwrite=True):
        location = directory + "/" + self.name + ".html"
        editFile = open(location, "w")
        editFile.write(self.html)
        editFile.close()
        
    # Updates the contents of the html to replace tokens    
    def update(self):
        self.html = self.html.replace("$title", self.title)
        self.html = self.html.replace("$content", self.content)

    # Loads a webpage template to pageList. If the filename specified is not valid,
    # a very basic page is loaded to the list.
    def loadTemplate(self, filename=""):
            try:
                    self.html = ""
                    loadFile = open(filename, "r")
                    for line in loadFile:
                            self.html = self.html + line
                    loadFile.close()
            except (IOError):
                    self.html = '''<html><head><title>$title</title></head>
                                   <body>$content</body></html>'''