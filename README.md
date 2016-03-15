Joseph Mulloy Demo Flask App
============================

Startup Instructions
====================
1. Start the Vagrant box

    vagrant up
2. Start the app via ssh with the following commands, the terminal must remain open for the app to run

    vagrant ssh
    cd /app
    python demo_app.py

Test Instructions
=================
In a separate terminal use the following commands to ssh to the vagrant box and run the test

    vagrant ssh
    cd /app
    python test.py
