
# Esri start of added imports
import sys, os, arcpy
# Esri end of added imports

# Esri start of added variables
g_ESRI_variable_1 = os.path.join(arcpy.env.packageWorkspace,u'apc_templates')
# Esri end of added variables

import sys, os, uuid, logging, json
import arcpy

# Config for Map Print
templateFolder = g_ESRI_variable_1

# logging 
FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
logging.basicConfig(filename=r'\\anadarko.com\world\AppsData\Houston\iMaps\Server\directories\arcgisoutput\Test\PrintTool_GPServer\Test_PrintTool\MapPrint_gp.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

# Input for Map Print
Web_Map_as_JSON = arcpy.GetParameterAsText(0)
logging.info("Web_Map_as_JSON: " + Web_Map_as_JSON)

webMap = json.loads(Web_Map_as_JSON)
# scan for token
token = None
for lyr in webMap["operationalLayers"]:
    if "url" in lyr:
        if lyr["url"].startswith("https://portalqa.anadarko.com/") == True:
            if "token" in lyr:
                token = lyr["token"]
# populate token for other ags layers
if token is not None:
    for lyr in webMap["operationalLayers"]:
        if "url" in lyr:
            if lyr["url"].startswith("https://portalqa.anadarko.com/") == True:
                if "token" not in lyr:
                    lyr["token"] = token
Web_Map_as_JSON = json.dumps(webMap)

# additional parameters
title = arcpy.GetParameterAsText(1)
logging.info("title: " + title)
size = arcpy.GetParameterAsText(2)
logging.info("size: " + size)
orientation = arcpy.GetParameterAsText(3)
logging.info("orientation: " + orientation)
format = arcpy.GetParameterAsText(4)
logging.info("format: " + format)
dpi_as_text = arcpy.GetParameterAsText(5)
logging.info("dpi_as_text: " + dpi_as_text)

# Retrieve the template file
tmplMxdName = size + "_" + orientation
logging.info("tmplMxdName: " + tmplMxdName)

tmplMxdPath = os.path.join(templateFolder, tmplMxdName + ".mxd")
if not os.path.exists(tmplMxdPath):
	arcpy.AddError("no such map template: %s"%tmplMxdPath)
	sys.exit()

# Calculate the print size in pixel
dpi = int(dpi_as_text)
widthAndHeight = size.split('x')
if len(widthAndHeight) != 2:
	arcpy.AddError("invalid map size: %s"%size)
	sys.exit()

if orientation == "Portrait":
	width = int(float(widthAndHeight[0]) * dpi)
	height = int(float(widthAndHeight[1]) * dpi)
elif orientation == "Landscape":
	width = int(float(widthAndHeight[1]) * dpi)
	height = int(float(widthAndHeight[0]) * dpi)
else:
	arcpy.AddError("invalid map orientation: %s"%orientation)
	sys.exit()

logging.info("width: " + str(width))
logging.info("height: " + str(height))

# Set Output FileName
outFileName = "mapPrint_%s.%s"%(str(uuid.uuid1()), format)
outFilePath = os.path.join(arcpy.env.scratchFolder, outFileName)

# Convert the web map to a map document
arcpy.AddMessage("Converting to a MapDocument...")

result = arcpy.mapping.ConvertWebMapToMapDocument(Web_Map_as_JSON, tmplMxdPath)
tmplMapDoc = result.mapDocument

df = arcpy.mapping.ListDataFrames(tmplMapDoc, 'Webmap')[0]


# Export Map
arcpy.AddMessage("Exporting to %s..."%format)

if format == "pdf":
	arcpy.mapping.ExportToPDF(tmplMapDoc, outFilePath, data_frame = df, resolution = dpi, df_export_width = width, df_export_height = height)
elif format == "jpg":
	arcpy.mapping.ExportToJPEG(tmplMapDoc, outFilePath, data_frame = df, resolution = dpi, df_export_width = width, df_export_height = height)
elif format == "png":
	arcpy.mapping.ExportToPNG(tmplMapDoc, outFilePath, data_frame = df, resolution = dpi, df_export_width = width, df_export_height = height)
else:
	arcpy.AddError("invalid export format: %s"%format)
	sys.exit()

# Set the output parameter to be the output file of the server job
Output_File = outFileName
logging.info("outFileName: " + outFileName)
arcpy.SetParameterAsText(6, Output_File)

arcpy.AddMessage("Print Completed")

# Clean up - delete the map document reference
tmplMapDoc_filePath = tmplMapDoc.filePath
del tmplMapDoc, result
os.remove(tmplMapDoc_filePath)



