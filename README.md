Joseph Mulloy Demo Flask App
============================

Startup Instructions
--------------------
1. Start the Vagrant box.

   ```bash
   vagrant up
   ```
2. Start the app via ssh with the following commands, the terminal must remain open for the app to run.

   ```bash
   vagrant ssh
   cd /app
   python demo_app.py
   ```

Test Instructions
-----------------
1. In a separate terminal use the following commands to ssh to the vagrant box and run the test.

    ```bash
    vagrant ssh
    cd /app
    python test.py
    ```
