import os
import re
import shutil
import requests

# Your TMDb API key
API_KEY = "README"

# Regex pattern to match folder name format
FOLDER_PATTERN = re.compile(r"^(.*?) \((\d{4})\) \{tvdb-(\d+)\}$")

# Regex to match "SxxExx" in file names
SEASON_EPISODE_PATTERN = re.compile(r"S(\d{2})E(\d{2})", re.IGNORECASE)

def get_tmdb_show(api_key, show_name, year=None):
    url = "https://api.themoviedb.org/3/search/tv"
    params = {
        "api_key": api_key,
        "query": show_name
    }
    if year:
        params["first_air_date_year"] = year
    response = requests.get(url, params=params)
    data = response.json()
    results = data.get("results")
    if not results:
        print(f"❌ No TMDb results for: {show_name} ({year})")
        return None
    return results[0]

def get_seasons(api_key, show_id):
    url = f"https://api.themoviedb.org/3/tv/{show_id}"
    params = {"api_key": api_key}
    response = requests.get(url, params=params)
    data = response.json()
    return data.get("seasons", [])

def rename_unpadded_season_folders(base_path):
    season_folder_pattern = re.compile(r'^Season (\d{1,2})$')
    for name in os.listdir(base_path):
        full_path = os.path.join(base_path, name)
        if os.path.isdir(full_path):
            match = season_folder_pattern.match(name)
            if match:
                season_num = int(match.group(1))
                padded_name = f"Season {season_num:02}"
                new_path = os.path.join(base_path, padded_name)
                if full_path != new_path and not os.path.exists(new_path):
                    os.rename(full_path, new_path)
                    print(f"🔄 Renamed '{name}' → '{padded_name}'")

def create_season_folders(base_path, seasons):
    for season in seasons:
        season_num = season.get("season_number")
        if season_num == 0:
            continue
        folder_name = f"Season {season_num:02}"
        folder_path = os.path.join(base_path, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"📁 Created: {folder_name}")
        else:
            print(f"✔️ Folder exists: {folder_name}")

def move_files_to_seasons(base_path):
    for filename in os.listdir(base_path):
        full_path = os.path.join(base_path, filename)
        if os.path.isfile(full_path):
            match = SEASON_EPISODE_PATTERN.search(filename)
            if match:
                season_num = match.group(1)
                dest_folder = os.path.join(base_path, f"Season {season_num}")
                if os.path.exists(dest_folder):
                    print(f"📂 Moving '{filename}' → '{dest_folder}'")
                    shutil.move(full_path, dest_folder)
                else:
                    print(f"⚠️ Season folder '{dest_folder}' not found. Skipping '{filename}'")
            else:
                print(f"⏭️ No SxxExx pattern in '{filename}'")

def process_all_show_folders(root_path):
    for folder_name in os.listdir(root_path):
        match = FOLDER_PATTERN.match(folder_name)
        if not match:
            continue

        show_name, year, tvdb_id = match.groups()
        folder_path = os.path.join(root_path, folder_name)
        if not os.path.isdir(folder_path):
            continue

        print(f"\n📺 Processing: {show_name} ({year}) [{tvdb_id}]")
        rename_unpadded_season_folders(folder_path)

        show = get_tmdb_show(API_KEY, show_name, year)
        if not show:
            continue

        seasons = get_seasons(API_KEY, show["id"])
        if not seasons:
            print("🚫 No seasons found.")
            continue

        valid_seasons = [s['season_number'] for s in seasons if s['season_number'] != 0]
        print(f"📊 Seasons found: {valid_seasons}")

        create_season_folders(folder_path, seasons)
        move_files_to_seasons(folder_path)

    print("\n✅ All done!")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    process_all_show_folders(current_dir)
