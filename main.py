from converter import convert

def main():
    # Ask the user for the ops level file
    OpsLevelFile = input("Enter the path to the OpsLevel service file: ")

    # Convert the ops level file to a datadog file
    DataDogService = convert(OpsLevelFile)

    # Write the datadog file to a new file
    if DataDogService:
        with open('service.datadog.yaml', 'w') as file:
            file.write(DataDogService)
        
        print(f"DataDog service file created successfully")


if __name__ == "__main__": 
    main()
