import os, smtplib, string, arcpy

# Variables for export path/PDF creation

Web_Map_as_JSON = arcpy.GetParameterAsText(0)
userName = arcpy.GetParameterAsText(1)
projectName = arcpy.GetParameterAsText(2)
templateMxd = arcpy.GetParameterAsText(3)
dpi = arcpy.GetParameterAsText(4)

# Convert the web map to a map document
arcpy.AddMessage("Converting to a MapDocument...")
result = arcpy.mapping.ConvertWebMapToMapDocument(Web_Map_as_JSON, templateMxd)
mxd = result.mapDocument

# Set File Names
pdfFileName = os.path.join(fullPath, projectName + '.pdf')
jpgFileName = os.path.join(fullPath, projectName + '.jpg')

#Export PDF
arcpy.AddMessage("Exporting to PDF...")
arcpy.mapping.ExportToPDF(mxd,pdfFileName, resolution = dpi)

# Email when script is complete
# Set variables for emailing log file
fromaddr = "iMapsPDF_NoReply@anadarko.com"
toaddrs  = userName + "@anadarko.com"
msg = "Path to PDF: file:" + pdfFileName + "\n\nJPEG Preview: file:" + jpgFileName + "\n\nPlease conserve paper by reviewing these documents before printing."

subj = 'PDF Job ' + projectName + ' has completed.'

body = string.join(("From: %s" % fromaddr, "To: %s" % toaddrs, "Subject: %s" % subj, "", msg), "\r\n")

server = smtplib.SMTP("mailrouter.anadarko.com","25")
server.sendmail(fromaddr, toaddrs, body)
server.quit()


