import util_functions
import boto3


client = boto3.client('resourcegroupstaggingapi')
paginator = client.get_paginator('get_resources')


def updateProjectFile():
    newProjects = util_functions.getProjectsInAWS()

    if not newProjects:
        print("No New Projects Given, operation closing")
        return
    projectsList = util_functions.pullData_file("projects.txt")

    newProjectSet = set()

    for project in newProjects:
        if project not in projectsList:
            projectsList.append(project)
            newProjectSet.add(project)
    projectsList.sort()
    #add updated projects list to file

    with open("projects.txt", "w+") as f:
        for p in projectsList:
            f.write(f"{p}\n")
    if newProjectSet:
        print(f"Project File Updated to include: {newProjectSet}")
    else:
        print("All Projects already found in catalog, no updates needed")
    return


def migrateProject():
    original = input("Enter Project you would like to migrate: ").strip()
    newName = input("Enter the new name for the Project: ").strip()

    ARN_list = list(util_functions.getProjectARNs(original))


    # Update (or create) tags for a resource
    if not ARN_list:
        print("No ARN's Found, no migration valid, terminating operation")
        return
    print(ARN_list)
    client.tag_resources(
        ResourceARNList=ARN_list,
        Tags={
            'project': newName,
        }
    )
