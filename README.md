# Dump1090 to TAK

Dump1090 to TAK is a Python script that retrieves aircraft data from Dump1090 and sends it as Cursor-on-Target (CoT) messages over UDP. It allows you to track and visualize aircraft positions in real-time using applications compatible with the TAK protocol.

## Features

- Fetches aircraft data from Dump1090 JSON API
- Converts aircraft data into CoT messages
- Sends CoT messages over UDP broadcast
- Includes a database for identifying military and civilian aircraft based on their ICAO addresses
- Prints aircraft data to the console for easy monitoring


Example of Terminal console UI.

![Console Preview](https://i.ibb.co/dbvQSB1/console-preview.jpg)

Example of tracks on WinTAK.

![WinTAK Preview](https://i.ibb.co/Xjg7hM3/Win-TAK-preview.jpg)


## Dev Notes
- ICAO military for Royal Canadian Air Force already added for my requirements
- I personally use a Raspberry Pi 4 with TAK Server, Dump1090-fa, and this script running automatically and it runs 24/7 with no issues
- I developed this script because adsbcot gave me plenty of issues, so I decided to make my own solution
- Currently looking for a public ICAO database with all military aircraft (https://www.ads-b.nl/) has many aircraft for a start state.

## Prerequisites

Before using this script, make sure you have the following installed:

- Python 3
- Requests library (can be installed via `pip3 install requests`)

## Usage

1. Make sure you have Dump1090 installed and running, providing access to the JSON data API.
   
2. Clone this repository `git clone https://github.com/bradleyrjhook/Dump1090-to-TAK.git` or download the `Dump1090_TO_CoT.py` to your local machine.

3. Navigate to the project directory `cd Dump1090-to-TAK`. Open the `sudo nano Dump1090_TO_CoT.py` script and modify the following variables:

   - `UDP_IP`: The broadcast address to send the CoT messages. By default, it is set to `"255.255.255.255"`.
   - `UDP_PORT`: The port number for the UDP communication. By default, it is set to `6969`.
   - `POLL_INTERVAL`: The interval (in seconds) between each data retrieval from Dump1090. By default, it is set to `3`.
   - `DUMP1090_URL`: The URL for accessing the Dump1090 JSON data. Modify it to match the address of your Dump1090 instance. By default, it is set to `"http://<your_dump1090_url>/data/aircraft.json"`. However, if Dump1090 is on your local machine, use `http://localhost:8080/data/aircraft.json`.
   - Modify the `mil_icao_database` dictionary in the script to include the ICAO addresses for military aircraft and their corresponding countries.
   - Modify the `mil_country_prefixes` dictionary in the script to include the country prefixes and corresponding cot types for military of specific nations.

4. Save the script.

5. Open a terminal or command prompt, navigate to the directory where the script is located, and run the following command to execute the script:

   ```bash
   python3 Dump1090_TO_CoT.py

The script will continuously fetch aircraft data, generate CoT messages, and broadcast them over UDP. The console will display the aircraft data in a table format for easy monitoring.

## Contributing
Contributions to the Dump1090 to TAK script are welcome! If you have any ideas, bug fixes, or improvements, feel free to submit a pull request or open an issue in this repository.

## License
This project is licensed under the MIT License.
