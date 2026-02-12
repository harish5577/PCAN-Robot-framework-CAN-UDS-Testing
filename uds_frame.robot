*** Settings ***
Library    PCANLibrary.py

*** Variables ***
@{TX_DATA}    0x11    0x12    0x13    0x14    0x15    0x16    0x17    0x18
@{TX_DATA1}    0x02    0x10    0x01  

*** Test Cases ***

Test Case 01: Single frame
    Initialize PCAN
    Send UDS Request    0x10    0x03
    ${RX_ID}    ${RX_DATA}=    Read UDS Response    expected_id=0x7EC
    Log    RX CAN ID: ${RX_ID}    console=True
    Log    RX CAN Data: ${RX_DATA}    console=True
    Uninitialize PCAN

Test Case 02:
    Initialize PCAN
    Log    TX CAN ID: 0x100    console=True
    Log    TX CAN Data: ${TX_DATA}   console=True
    Send CAN Single Frame    0x100    ${TX_DATA}
    Uninitialize PCAN

Test Case 03:
    Initialize PCAN
    Log    TX CAN ID: 0x201    console=True
    Log    TX CAN Data: ${TX_DATA1}    console=True
    Send CAN Single Frame    0x201    ${TX_DATA1}
    Uninitialize PCAN

Test Case 04: 
    Initialize PCAN
    Send UDS Request    0x10    0x01
    ${RX_ID}    ${RX_DATA}=    Read UDS Response    expected_id=0x7EC
    Log    RX CAN ID: ${RX_ID}    console=True
    Log    RX CAN Data: ${RX_DATA}    console=True
    Uninitialize PCAN