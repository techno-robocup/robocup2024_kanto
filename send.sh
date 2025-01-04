ssh ev3dev.local "rm -rf ~/robocup"
ssh ev3dev.local "mkdir ~/robocup"
scp -Cr . robot@ev3dev.local:~/robocup