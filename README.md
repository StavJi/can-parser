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
   python main.py

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
- TBD
 
## Project Structure
```
.
├── src/             # Source code
├── examples/        # Example input files
├── tests/           # Unit tests
├── requirements.txt # Project dependencies
├── .gitignore
└── README.md
```

## Roadmap
- [x] First project draft (proof of concept)
- [ ] Add support for custom CAN message definitions
- [x] Add oop
- [x] Add GUI
      
## Current project status
Make it more useful and less annoying to use

## Contributing
Contributions are welcome! Please fork the repository, create a feature branch, and submit a pull request.
