import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["pastpaperdb"]
mycol = mydb["pastpaperdata"]




#list all the subjects in a collection
def getSubjects(col=mycol):
  subjects = col.distinct("subject")
  return(subjects)

#list all units for a subject
def getUnits(subject,col=mycol):
  unit = col.distinct("unit",{"subject":subject})
  return (unit)

#list all years for a subject
def getYears(subject,unit,col=mycol):
  years = col.distinct("year",{"subject":subject,"unit":unit})
  return (years)



#get all sessions for a sibject for a year
def getSessions(subject,year,unit,col=mycol):
  sessions = col.distinct("session",{"subject":subject,"year":year,"unit":unit})
  return sessions


def getFile(subject,year,session,unit,col=mycol):
  file_dict = col.find({"subject":subject,"year":year,"session":session,"unit":unit,})
  return(file_dict)


#returns all links in the db
def getAllObjects(col=mycol):
  links = col.find()
  return links


