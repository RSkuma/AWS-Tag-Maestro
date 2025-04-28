import util_functions
import boto3
from collections import defaultdict
from datetime import datetime

client = boto3.client('resourcegroupstaggingapi')
paginator = client.get_paginator('get_resources')

def viewprojects():
    print("Listing Projects in File")
    projects = util_functions.pullData_file("projects.txt")
    projects.sort()
    print()
    for proj in projects:
        print(proj)


def viewProjectsInProd():
    '''
    Query AWS using the boto3 client to see all project tags on AWS resources
    '''

    print("Available Projects Found on AWS: ")
    print()
    setOfProjects = util_functions.getProjectsInAWS()
    print(setOfProjects)

def viewResourcesInProd():
    '''
    Query AWS using boto3 client, will find all resources with a project tag and display which resources are attached to said project
    '''
    print("Option 3: Viewing AWS Services in use by Projects")
    print()
    ServiceToProjectDict = defaultdict(list)
    for page in paginator.paginate():
        for resource_tag_map in page["ResourceTagMappingList"]:
            projectName = util_functions.parseTags(resource_tag_map["Tags"], "project")
            resourceType = util_functions.parseARN_resourceType(resource_tag_map["ResourceARN"])
            if projectName is not None:
                ServiceToProjectDict[resourceType].append(projectName)
    
    for resourceName in ServiceToProjectDict.keys():
        print(resourceName)
        for pName in ServiceToProjectDict[resourceName]:
            print(f"    {pName}")


def viewResourceTypes():
    print("Option 4: Viewing Types of resources Used in AWS Account")
    allResourceTypes = set()
    for page in paginator.paginate():
        for resource_tag_map in page["ResourceTagMappingList"]:
            allResourceTypes.add(util_functions.parseARN_resourceType(resource_tag_map["ResourceARN"]))
    print("All resources Found:")
    print(allResourceTypes)


def queryCosts():
    print("AWS Total Cost(Monthly Running Sum)")
    client = boto3.client('ce')

    # Get first and last day of the current month
    start = datetime.today().replace(day=1).strftime('%Y-%m-%d')
    end = datetime.today().strftime('%Y-%m-%d')
    response = client.get_cost_and_usage(
        TimePeriod={
            'Start': start,
            'End': end
        },
        Granularity='MONTHLY',
        Metrics=['UnblendedCost'],
        GroupBy=[
            {
                'Type': 'TAG',
                'Key': 'project'    # <-- Grouping by your "Environment" tag
            }
        ]
    )
    for group in response['ResultsByTime'][0]['Groups']:
        print(f"Project total costs for month: {start} to {end}")
        print(f"Cost: {group['Metrics']['UnblendedCost']['Amount']} USD")

def viewAll():
    print("Printing all Resource ARNs on Account")
    client = boto3.client('resourcegroupstaggingapi')
    paginator = client.get_paginator('get_resources')
    setOfARNs = set()
    for page in paginator.paginate():
        for resource_tag_map in page["ResourceTagMappingList"]:
            print(resource_tag_map)