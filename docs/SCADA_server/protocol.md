# SCADA server protocol

## List of available instructions

- CLOSE: Gracefully close the socket connection with the server
- DEF: Create or update a variable in the SCADA database
- DEL: Delete a variable from the database
- EXIT: Gracefully close the socket connection with the server
- GET: Return list of data from the scada logger with record date in UTC and data values separated by semi-colon
- HELP: Display help on the available instructions
- LIST: List available variables and local network devices on the SCADA database
- NET: Declare or update a local network device
- QUIT: Gracefully close the socket connection with the server

## Instruction CLOSE

Gracefully close the socket connection with the server

## Instruction DEF

Create or update a variable in the SCADA database

Usage: `DEF type variable description [options]`

with:

- type: type of the variable ('ard' for Arduino analog, 'lin' for linear transformation, 'exp' for exponential transformation)
- variable: the name of the variable to create/update
- description: a description of the variable (use quotes for more than one word)
- options: depends on the type of variable to define (see below)

### Description of variable types:

#### Arduino analog: 'ard'

There is no option to provide.

Example:

    DEF ard A0 "Analog input for sensor #0"

#### Linear transformation: 'lin'

Use an input variable X and apply a linear transformation with the equation `Y = a * X + b`

The 'options' group argument contains 3 arguments in this order:

- input variable X: the variable used for the calculation
- coefficient a: slope of the linear equation
- coefficient b: intercept of the linear equation

Example:

    DEF lin Y0 "Water depth at sensor #0" A0 0.001 -0.002

#### Exponential transformation: 'exp'

Use an input variable X and apply this equation `Y = a * (X - b) ^ c`

The 'options' group argument contains 4 arguments in this order:

- input variable: the variable used for the calculation
- coefficient a
- coefficient b
- coefficient c

Example for getting the discharge in l/s using King's triangular weir equation with a sill elevation of 10 cm:

    DEF exp Q0 "Discharge at sensor #0" Y0 0.014 10 2.5

#### Local network device: 'net'

The 'options' group argument contains 2 arguments:

- device name: the name of the device
- Order number of the variable on the device from 0 (0 for the first, 1 for the second...)

Example for getting the first variable of the device called "TEST_DEVICE":

    DEF net FIRST_DATA "The first data provided by the device" TEST_DEVICE 0

## Instruction DEL

Delete a variable from the database

Usage : `DEL [variable or local network device name]`

## Instruction EXIT

Gracefully close the socket connection with the server

## Instruction GET

Return list of data from the scada logger with record date in UTC and data values separated by semi-colon

Usage: `GET var1,var2`

Example: `GET R0,R1` returns `2018-10-22 11:50:53,092;58`

## Instruction HELP

Display help on the available instructions

Usage:

- `HELP`: list of available instructions
- `HELP [instruction]`: Documentation of an instruction

## Instruction LIST

List available variables and local network devices on the SCADA database

Usage:

- `LIST`: list available variables and devices
- `LIST [variable or device name]`: display details on a variable or a device

## Instruction NET

Declare or update a local network device

Usage: `NET device_name description number_of_variables`

With:

    - device_name: the name of the device (used after for declaring a variable with DEF net. See HELP DEF.)
    - description: Description of the device for human beings :)
    - number_of_variables: number of variables provided by the device

To define variables linked to the device, use the instruction `DEF net...`

## Instruction QUIT

Gracefully close the socket connection with the server
