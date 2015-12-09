
# Esri start of added imports
import sys, os, arcpy
# Esri end of added imports

# Esri start of added variables
g_ESRI_variable_1 = os.path.join(arcpy.env.packageWorkspace,u'apc_templates')
#g_ESRI_variable_2 = os.path.join(arcpy.env.packageWorkspace,u'map_export')
# Esri end of added variables

import sys, os, uuid
import arcpy

# Config for Map Print
templateFolder = g_ESRI_variable_1
#exportFolder = g_ESRI_variable_2

# Input for Map Print
## Web_Map_as_JSON is the variable used by the PrintTask so it needs to be exact
Web_Map_as_JSON = arcpy.GetParameterAsText(0)
## Other params are additional so they needs to match the input params in the tool properties
title = arcpy.GetParameterAsText(1)
size = arcpy.GetParameterAsText(2)
orientation = arcpy.GetParameterAsText(3)
format = arcpy.GetParameterAsText(4)
dpi_as_text = arcpy.GetParameterAsText(5)

arcpy.AddMessage("parameter Layout_Template: ")

# Retrieve the template file
tmplMxdName = size + "_" + orientation
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
## Output_File is the variable used by the PrintTask so it needs to be exact
## Output_File is just a file name. AGS adds a proper URL path before returning its value
Output_File = outFileName
arcpy.SetParameterAsText(6, Output_File)

arcpy.AddMessage("Print Completed")

# Clean up - delete the map document reference
tmplMapDoc_filePath = tmplMapDoc.filePath
del tmplMapDoc, result
os.remove(tmplMapDoc_filePath)



