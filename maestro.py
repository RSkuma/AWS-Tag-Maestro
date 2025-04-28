import sys
import boto3
import util_functions
import query_functions
import transform_functions

client = boto3.client('resourcegroupstaggingapi')
paginator = client.get_paginator('get_resources')

def option_summary():
    with open('intro.txt', encoding="utf-8") as f:
        read_data = f.read()
        print(read_data)

def option_close_maestro():
    sys.exit(0)
def invalid_option():
    print("Invalid option. Please choose a valid Option")

# Map numbers to functions
options = {
    '0': option_summary,
    '1': query_functions.viewprojects,
    '2': query_functions.viewProjectsInProd,
    '3': query_functions.viewResourcesInProd,
    '4': query_functions.viewResourceTypes,
    '5': transform_functions.updateProjectFile,
    '6': transform_functions.migrateProject,
    '7': query_functions.viewAll,
    '8': query_functions.queryCosts,
    '9': option_close_maestro,
}

def main():


    print("=======================")
    print(" Welcome to the AWS Tag Maestro")
    print("Please choose an option:")
    print("[0] Introduction")
    print("[1] View Projects on File")
    print("[2] View Projects in Production")
    print("[3] Service to Project Breakdown")
    print("[4] Show AWS Resource Types in Production")
    print("[5] Update Projects on File")
    print("[6] Migrate Project")
    print("[7] View Resources Dumps in AWS")
    print("[8] Check Costs")
    print("[9] Exit Maestro")
    print("=======================")

    choice = input("Enter Option: ").strip()
    # Call the appropriate function or fallback to invalid_option
    func = options.get(choice, invalid_option)
    func()

if __name__ == "__main__":
    while True:
        main()
        for i in range(3):
            print("")
