# How to place orders electronically via the JockMKT api with no coding experience:

1. Download and install python

    [DOWNLOAD AND INSTALL PYTHON](https://www.python.org/downloads/)

2. open your terminal (windows: Ctrl + Shift + P, mac: search + open terminal)

3. In your terminal type:

    ``pip install pandas``

    ``pip install jockmkt-sdk``

    ``pip install numpy``

    if this doesn't work, preface each line with ``python3 -m``

4. Make sure you get your API keys from developers@jockmkt.com

5. Go to the JockMKT web app and choose your event.
    - Adjacent to the name of the event, above the players, is a small image of a sheet with "csv" on it. Download this CSV.

6. Open this CSV in Excel

7. Add two columns: One titled "price" and one titled "quantity" (Ensure that they are all lowercase, or this will not work.)
    - Add prices and quantities for every player that you want to place a bid on. 
        - ***LEAVE price, quantity BLANK FOR ANY player YOU DO NOT WANT TO BID ON***
    - Save the file somewhere you'll be able to find it!
    - **DO NOT CHANGE FILE NAME**

8. Insert your secret and api keys between the quotation marks on lines 6 and 7 (api_key, secret_key)
    - Your *API key* starts with "jm_key"
    - Your *secret key* is a string of length 32, made of random numbers and letters

9. Insert the path to your CSV between the quotation marks on line 11 (path_to_csv)
    - FINDING YOUR FILEPATH:
        [MAC](https://support.apple.com/guide/mac-help/get-file-folder-and-disk-information-on-mac-mchlp1774/mac)
        [WINDOWS](https://www.softwareok.com/?seite=faq-Windows-10&faq=40)

10. Decide whether you want the script to sleep until just before the event before placing your orders:
    - On line 15: 
        - sleep = True if you want to sleep
        - sleep = False if you do not want to sleep

11. Run the script! How to do this depends on your text editor. I recommend Visual Studio Code.

12. If you choose to download VSCode, I suggest the Jupyter Notebook extension.
    [GET VS CODE](https://code.visualstudio.com/download)
    
