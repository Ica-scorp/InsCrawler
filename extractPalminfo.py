
def getEvent(event_info):

    # Split the event_info into lines
    lines = event_info.split('\n')

    # Extract relevant information from each line
    event_name = lines[0].strip('* ').strip()  # Remove leading '*' and whitespace
    event_date = lines[1].split(': ')[1].strip()  # Extract the date part
    event_time = lines[2].split(': ')[1].strip()  # Extract the time part
    event_location = lines[3].split(': ')[1].strip()  # Extract the location part

    # Print the extracted information
    print("Event Name:", event_name)
    print("Event Date:", event_date)
    print("Event Time:", event_time)
    print("Event Location:", event_location)

