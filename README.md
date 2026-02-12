# PCAN Robot Framework UDS Testing

This project contains Robot Framework test automation scripts for CAN and UDS testing using PCAN hardware.

## Features
- UDS Session Control Testing
- Single Frame CAN Transmission
- PCAN initialization and cleanup
- Automated response validation

## Test Cases
- UDS Diagnostic Session Control (0x10)
- Raw CAN Single Frame Transmission
- Response validation with expected CAN ID

## Requirements
- Python 3.x
- Robot Framework
- PCAN Hardware
- PCANBasic API

## Install Dependencies

```bash
pip install -r requirements.txt
