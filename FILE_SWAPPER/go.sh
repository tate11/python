#!/bin/bash

sudo rm -rf /home/alii2/poo/fs2/*.*
sudo rm -rf /home/alii2/poo/fs/*.*
sudo rm -rf /tmp/sprott/*.*
sudo cp /home/alii2/poo/fs2.pdf /home/alii2/poo/fs2
sudo cp /home/alii2/poo/fs1.pdf /home/alii2/poo/fs
sudo python Driver.py --i1=/home/alii2/poo/fs/fs1.pdf --i2=/home/alii2/poo/fs2/fs2.pdf -s /tmp/sprott/
sudo python Driver.py --i1=/home/alii2/poo/fs/fs2.pdf --i2=/home/alii2/poo/fs2/fs1.pdf -s /tmp/sprott/
