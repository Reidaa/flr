# FLR

## Description
FLR (From Left to Right) is a general purpose trading bot.

## READ BEFORE USE
1. If you don't enable `TEST_MODE`, you will be using REAL money.
2. To ensure you do not do this, ALWAYS check the `TEST_MODE` variable in `config.yml`.

## Usage

1. Install Dependencies
    - Easy mode (might clash with current deps)
        ```sh
        pip install -r requirements.txt
        ```
    - Preferred Method (venv)
        ```sh
        python3 -m venv .venv
      
        source .venv/bin/activate # linux
        .\.venv/scripts/activate # windows
    
        pip install -r requirements.txt
        ```


2. Copy `creds.example.yml` to `creds.yml` (or whatever you want.) and update the creds.

    ```sh
    # linux: Copy file over.
    cp creds.example.yml creds.yml

    # windows: either copy the file in explorer and rename to 'creds.yml' or use
    copy creds.example.yml creds.yml
    
    # powershell
    Copy-Item creds.example.yml -Destination creds.yml
    ```
    
    - Edit `creds.yml`.
    


3. Configure input params as in `config.yml`
     

4. Run the script
    - Standard 
        ```sh
        python3 flr.py
        ```
    - Background process (**linux only**)
        ```sh
        nohup python3 -u flr.py >> log.txt 2>&1 &
        ```
        The logs are stored in log.txt. To stop the process either look in your process list with `ps aux | grep -i python3` and kill with `kill PROCESS_ID` or `killall python3` when you know what you're doing.


5. Use the `--help` flag if you want to see supported arguments

## 💥 Disclaimer

All investment strategies and investments involve risk of loss. 
**Nothing contained in this program, scripts, code or repositoy should be construed as investment advice.**
Any reference to an investment's past or potential performance is not, 
and should not be construed as, a recommendation or as a guarantee of 
any specific outcome or profit.
By using this program you accept all liabilities, and that no claims can be made against the developers or others connected with the program.
