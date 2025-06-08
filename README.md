# SonarrQuickSeasons
Create Season Folders Inside TVShows folder.


SonarrQuickSeasons was designed by ChatGPT starting from a .bat file all the way to a fully automated Python script in under one hour. Through SonarrQuickSeasons you can easily organize your entire TVShow library in under 5 minutes. The way the script works is it uses an **API Key** from TMDB and parses through all your shows. 

### WARNING!
All show files must be formatted "Show Name (YYYY)" **EXAMPLE** Brooklyn Nine-Nine (2013). For organization, individual shows must have **S##E##** **Example** Brooklyn Nine-Nine (2013) - S02E01 or simply **S02E01**. If your files are not labeled as such this will not work! 

**We are not liable for broken shows!**


### INSTRUCTIONS:
**REQUIRED:**
Create an account at www.themoviedb.org and then grab **API Key** from https://www.themoviedb.org/settings/api. Replace the **README** inside CreateSeasons.py with your **API Key**!

#### Windows:
1. Copy CreateSeasons.py and Replace the **README** inside CreateSeasons.py with your **API Key** if you have not done so already.
2. Place CreateSeasons.py inside your **/TVShows** folder.
3. Install python through the windows store.
4. Open CMD or PowerShell.
5. Run "python -m ensurepip --upgrade"
6. Run "python -m pip install requests"
7. CD to folder where your Network share is located. **EXAMPLE** cd Z:/Unraid/Plex_Media/TVShows
8. Run "python .\CreateSeasons.py"
9. Watch as all your shows get organized

#### Linux:
1. Copy CreateSeasons.py and Replace the **README** inside CreateSeasons.py with your **API Key** if you have not done so already.
2. Place CreateSeasons.py inside your **/TVShows** folder.
3. 
