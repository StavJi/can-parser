# CAN bus message parser
This project is a tool for parsing J1939 CAN bus messages stored in log files.
It is designed to help developers and engineers analyze raw CAN traffic, decode messages, and work with structured data for further processing or visualization.

## Features
- Load CAN bus data from files
- Parse raw frames into structured messages
- Support for customizable message definitions

## Getting Started

### Prerequisites
- Python 3.x
- Dependency management via `requirements.txt` file  

### Usage
- Clone the repository
- Install dependencies
    ```bash
    pip install -r requirements.txt
- Run application 
   ```bash
   python src/main.py
- Select file to parse
- Enjoy!

### Example Input
Raw CAN log file (CSV-like), in following format Timestamp [ms], Message ID, Data lenght, Can bus data, Channel:

```
000000021352 0x18ff08fe 8 000071FFFFFFFFFF ch=2
000000021353 0x18ff20fe 8 00000000FFFFFFFF ch=2
000000021353 0x18ff0cfe 8 00F00000FFFFFFFF ch=2
000000021356 0x18ff08fe 8 010071FFFFFFFFFF ch=1
000000021357 0x18ff20fe 8 00000000FFFFFFFF ch=1
```

### Example Output
#### *.txt
```
Timestamp=000000083718; Frame=TMCSTATUS; Channel=1
 tmc_state=0; tmc_dt=DATE: 01.09.2025 TIME: 08:30; dplus=1
Timestamp=000000084021; Frame=ACUSTATUS2; Channel=1
 acu_supply_1=23.75
Timestamp=000000084236; Frame=TMCSTATUS; Channel=1
 tmc_state=0; tmc_dt=DATE: 01.09.2025 TIME: 08:30; dplus=1
Timestamp=000000084528; Frame=ACUSTATUS2; Channel=1
 acu_supply_1=23.75
Timestamp=000000084754; Frame=TMCSTATUS; Channel=1
```
#### *.xlsx
 TBD
## Project Structure
```
.
├── examples/        # Example input files
├── src/             # Source code
├── tests/           # Unit tests
├── .gitignore
├── README.md
└── requirements.txt # Project dependencies
```

## Current project status
Refactoring GUI, so it remains responsive and doesn’t hang during long execution.

## Contributing
Contributions are welcome! Please fork the repository, create a feature branch, and submit a pull request.
