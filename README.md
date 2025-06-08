# SonarrQuickSeasons
Create Season Folders Inside TVShows folder.


So quick disclaimer! I created this automation script due to an issue that many probably face. I was running Overseerr and forgot to check the "Seasons" checkbox when setting up Sonarr on Overseerr. This then caused Sonarr to create show folders WITHOUT any season folders. This might not be an issue for many but for my OCD it definitely caused an issue. Any time I would go to check my folders to make sure things were going right, or to delete a season that downloaded wrong, I would be met with a show folder that just had 20 episode files that were not in any season folders, which makes it a heck of a lot harder to manage your seasons. So I decided lets see what ChatGPT has to offer on this one. I used to program heavily in Java, C++, C#, and web-based code, although for this I did not want to sit and create a silly little script for 5 hours. Thus came a batch script that created the Season folders based on how many seasons I told the batch file to make. Next thing I knew I had a Python file that connected to TMDB API and was getting everything for me. One prime example where ChatGPT can come in handy. Now if you read this you're an interesting person. On to the information for the program.

::
SonarrQuickSeasons was designed by ChatGPT starting from a .bat file all the way to a fully automated Python script in under one hour. Through SonarrQuickSeasons you can easily organize your entire TVShow library in under 5 minutes. The way the script works is it uses an **API Key** from TMDB and parses through all your show folders, creates all the seasons based on that show, and then moves all your show files into their season folders based on file name using the SxxExx format. All your season folders will have a leading zero so make sure you change Sonarr Media Management Settings for Season Folder Format to Season {season:00}.

### WARNING!
All show files must be formatted "Show Name (YYYY)" **EXAMPLE** Brooklyn Nine-Nine (2013). For organization, individual shows must have **SxxExx** **Example** Brooklyn Nine-Nine (2013) - S02E01 or simply **S02E01**. If your files are not labeled as such this will not work! **Please make sure that Sonarr Media Management Settings for Season Folder Format is set to Season {season:00}!**

**We are not liable for broken shows if your files are not labeled correctly!**


### INSTRUCTIONS:
**REQUIRED:**
Create an account at www.themoviedb.org and then grab **API Key** from https://www.themoviedb.org/settings/api. Replace the **README** inside CreateSeasons.py with your **API Key**!

#### Windows:
1. Copy CreateSeasons.py and Replace the **README** inside CreateSeasons.py with your **API Key** if you have not done so already.
2. Place CreateSeasons.py inside your **/TVShows** folder. **EXAMPLE** Z:/Unraid/Plex_Media/TVShows/CreateSeasons.py
3. Install Python through the Windows store.
4. Open CMD or PowerShell.
5. Run "python -m ensurepip --upgrade"
6. Run "python -m pip install requests"
7. CD to the folder where your Network share is located. **EXAMPLE** cd Z:/Unraid/Plex_Media/TVShows
8. Run "python .\CreateSeasons.py"
9. Watch as all your shows get organized

#### Linux:
1. Navigate using "CD" to where your **TVShow Library** is located. **Example cd /mnt/PlexMedia/TVShows**
2. Use "wget https://raw.githubusercontent.com/SleepingPanda4/SonarrQuickSeasons/refs/heads/main/CreateSeasons.py" to copy CreateSeason.py file to the directory.
3. Then add your **API Key** to the file using "nano CreateSeason.py" and replace **README** next to **API_KEY** on line 7 with your **API KEY** from https://www.themoviedb.org/settings/api.
4. Check if Python is installed "**python3 --version**" if not run **"sudo apt install python3"**
5. Create Python Virtual Environment "python3 -m venv venv"
6. Activate Virtual Environment "source venv/bin/activate"
7. Install pip requests "pip install requests"
**By running this in a virtual environment you prevent creating errors in your system from Python**
8. Now just run the Python script "python ./CreateSeasons.py"
**The next time you run the script:**
1. Run "source venv/bin/activate"
2. Now just run the Python script as usual "python ./CreateSeasons.py"


You can create this into a CronTab job to run weekly.

