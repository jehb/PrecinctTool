# GIS 540 Final Project
# All code by Jason Baker (jebaker3@ncsu.edu) unless otherwise noted.

import arcpy, os, sys

p = os.path.dirname(sys.argv[0])
p = os.path.dirname(p)
sys.path.append(p)

# Import my custom-coded classes
import precinctclass, webpageclass
    
# Input variables - for release
'''baseDirectory = os.path.dirname(sys.argv[0])
precinctFile = sys.argv[1]
precinctFieldName = sys.argv[2]
pollingFile = sys.argv[3]
pollingFieldName = sys.argv[4]
precinctMap = sys.argv[5]
outDirectory = sys.argv[6]'''

# Input variables - for testing outside ArcGIS
baseDirectory = os.path.dirname(sys.argv[0])
precinctFile = r"\\wishbone.oit.ncsu.edu\ceo$\classes\GIS540\jebaker3\data\Voting_Precincts.shp"
precinctFieldName = "NAME"
pollingFile = r"\\wishbone.oit.ncsu.edu\ceo$\classes\GIS540\jebaker3\data\precinctpolls.shp"
pollingFieldName = "STATION"
templateFile = ""
precinctMap = r"\\wishbone.oit.ncsu.edu\ceo$\classes\GIS540\jebaker3\jebaker3.mxd"
outDirectory = r"c:\temp"

# Set environment workspace to the base directory, allow overwrites
arcpy.env.workspace = outDirectory
arcpy.env.overwriteOutput = 1

# Calculate centroids shapefile, convert to layer and add to map
arcpy.AddMessage("Calculating precinct centers...")
centroidsFile = outDirectory + "/Centroids.shp"
arcpy.FeatureToPoint_management(precinctFile, centroidsFile)

inMemLyr = "Centroids"
onDiskLyr = outDirectory + "/Centroids.lyr"
arcpy.MakeFeatureLayer_management(centroidsFile, inMemLyr)
'''arcpy.SaveToLayerFile_management(inMemLyr, onDiskLyr)
layerToAdd = arcpy.mapping.Layer(onDiskLyr)
mxd = arcpy.mapping.MapDocument(precinctMap)
dfs = arcpy.mapping.ListDataFrames(mxd)
df = dfs[0]
arcpy.mapping.AddLayer(df, layerToAdd)'''

arcpy.SetParameterAsText(6, centroidsFile)

# Use FeatureToPoint function to find a point inside each park

# Create list of precinct objects
precinctList = []
sc = arcpy.SearchCursor(precinctFile)
for line in sc:
    name = line.Name
    id = line.FID
    precinctList.append(precinctclass.precinct(name, id))
del line
del sc

# Create map images
'''
arcpy.AddMessage("Creating precinct images...")
imageMap = arcpy.mapping.MapDocument(precinctMap)
for pageNum in range(1, imageMap.dataDrivenPages.pageCount + 1):
    imageMap.dataDrivenPages.currentPageID = pageNum
    imageLocation = outDirectory + "/" + precinctList[pageNum-1].webname + ".png"
    arcpy.mapping.ExportToPNG(imageMap, imageLocation)
del imageMap'''

# Write precinct webpages
arcpy.AddMessage("Creating precinct webpages...")
for precinct in precinctList:
    precinctPage = webpageclass.webpage(precinct.webname, precinct.name, "")
    precinctPage.loadTemplate()
    precinctPage.content = '''<center><h1>%s</h1><img src="%s"></center>%s has an area of %s acres. Click <a
                         href="index.html">here</a> to go back to the main
                         page.''' % (precinct.name, precinct.imagename, precinct.name, precinct.getAcres(precinctFile))
    precinctPage.update()
    precinctPage.write(outDirectory)

# Write main page.
arcpy.AddMessage("Creating index page...")
mainPage = webpageclass.webpage("index", "Orange County Precincts Information", "")
mainPage.loadTemplate()
content = "Welcome to my website!\n"
for precinct in precinctList:
    content = "%s<li><a href=\"%s.html\">%s</a></li>\n" % (content, precinct.webname, precinct.name)
content = content + "</ul>\n"
mainPage.content = content
mainPage.update()
mainPage.write(outDirectory)