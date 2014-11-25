import arcpy, re

class precinct:
    def __init__(self, name, id):
        # Returns titlecase. Borrowed from Python docs:
        # http://docs.python.org/library/stdtypes.html
        self.name = re.sub(r"[A-Za-z]+('[A-Za-z]+)?",
                      lambda mo: mo.group(0)[0].upper() +
                                 mo.group(0)[1:].lower(),
                          name)
        self.id = id
        self.webname = self.name.lower().replace("'","").replace(" ","").replace(".","")
        self.imagename = self.webname + ".png"
    
    def getAcres(self, precinctFile):
        # Create an acres field if it doesn't have one
        hasAcreField = False
        fields = arcpy.ListFields(precinctFile)
        for field in fields:
            if field.name == "AcreArea":
                hasAcreField = True
        if hasAcreField == False:
            arcpy.AddField_management(precinctFile, "AcreArea", "Float", 8)
            # Calculate the area in acres.
            arcpy.CalculateField_management(precinctFile, "AcreArea", "!shape.area@acres!", "PYTHON")
        # Load area into precinctAreaAcresList
        sc = arcpy.SearchCursor(precinctFile)
        for line in sc:
            if line.FID == self.id:
                acreage = line.AcreArea
        del line
        del sc
        return acreage