# KAGGLE_ETL_PIPELINE

This is an ETL pipeline that, downloads data from a kaggle competition inserts it into a mysql database and then lets you build graphs over some columns of the data.


# INSTRUCTIONS

* you first need to login to your kaggle account and get the api token from there, a json file will be downloaded, save it to c:/users/'your user'/.kaggle*
* then install mysql, installer file given, install full package of mysql, follow on screen instructions and then set password to '123456'
* now open a commandprompt (cmd), navigate to the project directory and add this command, ' pip install --upgrade -r requirements.txt '
* after the libraries are installed, in the same (cmd) type the command ' streamlit run st.py'  , if the command fails to run kindly restart the computer and then do this step
* the program will take around 10-12 mins for the initial setup (it downloads the dataset directly from kaggle and then populates the database when you run it for the very first time) after the initial setup, it won't take so much time to run




# NOTE

This was a client specific project and was catered as such, it downloads the files from a specific kaggle competition and then inserts into the database as required. 
