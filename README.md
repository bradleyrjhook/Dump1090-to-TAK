# Dump1090-to-TAK

Dump1090 to TAK is a Python script that retrieves aircraft data from Dump1090 and sends it as Cursor-on-Target (CoT) messages over UDP. It allows you to track and visualize aircraft positions in real-time.

## Features

- Fetches aircraft data from Dump1090 JSON API
- Converts aircraft data into CoT messages
- Sends CoT messages over UDP broadcast
- Includes a database for identifying military and civilian aircraft based on their ICAO addresses
- Prints aircraft data to the console for easy monitoring
- Supports both HTTP and local file data sources for aircraft data

Example of Terminal console UI.

![Console Preview](https://i.ibb.co/ctyxMHt/console-preview2.jpg)

Example of tracks on WinTAK.

![WinTAK Preview](https://i.ibb.co/wJTGY7Z/Win-TAK-preview-2.jpg)

## Dev Notes
- ICAO military for Royal Canadian Air Force already added for my personal requirements
- I personally use a Raspberry Pi 4 with TAK Server, Dump1090-fa, and this script running automatically and it runs 24/7 with no issues
- I developed this script because `adsbcot` gave me plenty of issues, so I decided to make my own solution
- Currently looking for a public ICAO database with all military aircraft (https://www.ads-b.nl/) has many aircraft for a start state.

## Requirements

- Python 3.6 or higher
- Requests library (for HTTP data source)
- `Dump1090` server running and providing aircraft data

## Installation

1. Install the required dependencies:
    ```bash
    pip3 install requests

2. Clone the repository:
    ```bash
    git clone https://github.com/bradleyrjhook/Dump1090-to-TAK.git

## Usage

1.	Navigate to the project directory:
    ```bash 
    cd Dump1090-to-TAK
2. Open the script and modify the following variables:
    ```bash
    sudo nano Dump1090_to_TAK.py
3.	Set the configuration variables at the top of the file:
      - `UDP_IP`: The broadcast address to send the CoT messages. By default, set to `"255.255.255.255"`.
      - `UDP_PORT`: The port number for the UDP communication. By default, set to `6969`.
      - `POLL_INTERVAL`: The interval (in seconds) between each data retrieval from Dump1090. By default, set to `3`.
      - `DUMP1090_URL`: The URL for accessing the Dump1090 JSON data. Modify it to match the address of your Dump1090 instance. By default, it is set to
        `http://localhost:8080/data/aircraft.json"`.
4.	Define the `mil_icao_database` and `mil_country_prefixes` dictionaries according to your requirements.
5.	Save the changes to the file.
6.	Run the script:
	```bash
	python3 Dump1090-to-TAK.py
	
The script will start retrieving aircraft data, filtering military aircraft, and sending CoT messages over UDP.

##	Configuration

### UDP Configuration
The following configuration variables control the UDP settings:
- `UDP_IP`: The UDP broadcast address. Set it to the appropriate value for your network configuration.
- `UDP_PORT`: The UDP port to send CoT messages to.

###	Data Source Configuration
The script supports two types of data sources: HTTP and local file.

- HTTP Data Source
  
	To use an HTTP data source, set the `DUMP1090_URL` variable to the URL of the aircraft data source provided by DUMP1090. For example:
	`DUMP1090_URL = "http://10.0.0.209:8080/data/aircraft.json"`
	
- Local File Data Source

	To use a local file as the data source, set the `DUMP1090_URL` variable to the file URL using the `file://` scheme. For example:
	`DUMP1090_URL = "file:///home/dump1090/dump1090-json/aircraft.json"`
	
	Make sure to replace the file path with the actual path to your aircraft data file.

##	Filtering Configuration
The script provides filtering capabilities for military aircraft based on ICAO codes. The `mil_icao_database` dictionary defines the ICAO codes for different aircraft types. Update this dictionary according to your requirements.

The `mil_country_prefixes` dictionary defines the country prefixes associated with military aircraft. Update this dictionary to include the appropriate country prefixes and their corresponding CoT types.

##	Contributing
Contributions to the project are welcome. Feel free to open issues for bug reports or feature requests, and submit pull requests with improvements.

##	License
This project is licensed under the MIT License. See the LICENSE file for more details.
