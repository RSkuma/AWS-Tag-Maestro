import boto3
import util_functions

def parseARN_resourceType(arn: str):
    arn_segments = arn.split(":")
    service = arn_segments[2]
    return service
def parseARN_region(arn: str):
    arn_segments = arn.split(":")
    region = arn_segments[3]
    return region
def parseTags(tags, targetTag):
    localDict = dict()
    for keyval in tags:
        localDict[keyval["Key"]] = keyval["Value"]
    if "project" in localDict:
        return localDict[targetTag]
    else:
        #print ("No Tag [{tagname}] Detected".format(tagname = targetTag) )
        return None

def getProjectARNs(targetProjectName):
    client = boto3.client('resourcegroupstaggingapi')
    paginator = client.get_paginator('get_resources')
    setOfARNs = set()
    for page in paginator.paginate():
        for resource_tag_map in page["ResourceTagMappingList"]:
            projectName = parseTags(resource_tag_map["Tags"], "project")
            if projectName is not None and projectName == targetProjectName:
                setOfARNs.add(resource_tag_map["ResourceARN"])
        
    print("-------------------")
    return setOfARNs



def pullData_file(filename: str):
    with open(filename, encoding="utf-8") as fileObj:
        lines = fileObj.readlines()
    return [line.rstrip('\n') for line in lines]

def getProjectsInAWS():
    client = boto3.client('resourcegroupstaggingapi')
    paginator = client.get_paginator('get_resources')
    setOfProjects = set()
    for page in paginator.paginate():
        for resource_tag_map in page["ResourceTagMappingList"]:
            projectName = util_functions.parseTags(resource_tag_map["Tags"], "project")
            if projectName is not None:
                setOfProjects.add(projectName)
    return setOfProjects