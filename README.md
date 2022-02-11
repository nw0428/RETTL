# RETTL
A repository for RETTL code


## Instructions for Feb 11
1. Plug a motor into the A slot on spike prime with a bar attached to its output so it is easier to spin it.
1. Plug the color sensor into the D slot on spike prime
1. Plug spike prime into your laptop and open a new python project in the LEGO SPIKE app
1. Copy the code from robot-agents/feb11.py into the python project and upload the code to spike
1. Close the spike prime app
1. Download basicserial.py from this repository
1. `pip3 install pyserial` or `pip install pyserial`

### For data over USB
Run `python basicserial.py` to see the training and current data. Choose the appropriate USB port when prompted


### For data over bluetooth
The bluetooth connection is tricky
1. Remove the battery from spike prime
1. Open bluetooth settings and delete your spike prime
1. Replace the battery in spike prime, turn it on, and touch the bluetooth button
1. Re-add and connect with spike prime 
1. Run `python basicserial.py` to see the training and current data


## Run program 0 on spike prime
You make choices by cycling with the right and left button. Then tap the spike prime to select.
1. Choose (right left button) the X if you want to use the default training set
** Then the screen will go blank
1. Choose the check mark if you want to train
1. In training mode you can choose between the chess board (continue training) and the X (finish training)
1. To train, set the angle you want on the motor, point the color sensor at the color you want to train with, and then tap spike prime.
1. Once you choose X the screen will go blank.
