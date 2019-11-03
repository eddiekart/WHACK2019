Intended use: Current induced in circuit by RFID reader demonstrates RFID card security by showing that
	having a button that completes the circuit only when pressed would prevent data on the card being
	read unintentionally

Demonstration of a user-created circuit break that disallow reading of RFID cards unless intended through the use 
of a button.
Pressing the button would complete the circuit, allowing current to be induced by a RFID reader, sending the data
to be read.

Effects: Increases security of the data on card

Circuit:
    _____Button  _______________________
    |           ______|______           |
    |           |            |          | 
Inductor    Capacitor    Capacitor     LED
    |           |____________|          |
    |__________________|________________|