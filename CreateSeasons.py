import os
import re
import shutil
import requests
import stat

RED = '\033[0;31m'
RESET = '\033[0m'

CONFIG_FILE = "tvdb_api_key.conf"

def load_config():
    config = {}
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    key, val = line.split("=", 1)
                    config[key.strip()] = val.strip()
    return config

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        for key, val in config.items():
            f.write(f"{key}={val}\n")

def load_api_key_and_format():
    config = load_config()
    api_key = config.get("api_key")
    season_format = config.get("season_folder_format")

    if not api_key:
        api_key = input("Enter your TVDb API key: ").strip()
        config["api_key"] = api_key
        save_config(config)
        print(f"🔑 Saved TVDb API key to {CONFIG_FILE}")
    else:
        print(f"🔑 Loaded TVDb API key from {CONFIG_FILE}")

    use_leading_zero = None
    if season_format in ("1", "2"):
        print(f"\nSaved season folder format found: {season_format} ({'With leading zero' if season_format == '1' else 'Without leading zero'})")
        resp = input("Are these settings correct? (y/n): ").strip().lower()
        if resp == "y":
            use_leading_zero = (season_format == "1")

    if use_leading_zero is None:
        print()  # empty line before prompt
        print("Choose how season folders should be named:")
        print(f'{RED}To find this setting go to Media Management in Sonarr Settings and find "Season Folder Format".{RESET}')
        print("1) With leading zero (Season 01, Season 02, ...)")
        print("2) Without leading zero (Season 1, Season 2, ...)")
        choice = input("Enter 1 or 2: ").strip()
        while choice not in ("1", "2"):
            choice = input("Please enter 1 or 2: ").strip()
        use_leading_zero = choice == "1"

        save_choice = input("Would you like to save this season folder format for later? (y/n): ").strip().lower()
        if save_choice == "y":
            config["season_folder_format"] = choice
            save_config(config)
            print(f"💾 Saved season folder format to {CONFIG_FILE}")

    return api_key, use_leading_zero

def inherit_permissions(child_path, parent_path):
    stat_info = os.stat(parent_path)
    try:
        os.chown(child_path, stat_info.st_uid, stat_info.st_gid)
    except PermissionError:
        print(f"⚠️ Permission denied changing ownership for {child_path}. Skipping chown.")
    except AttributeError:
        # os.chown might not be available on Windows
        pass
    os.chmod(child_path, stat.S_IMODE(stat_info.st_mode))

FOLDER_PATTERN = re.compile(r"^(.*?) \((\d{4})\)")
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

def rename_unpadded_season_folders(base_path, use_leading_zero):
    season_folder_pattern = re.compile(r'^Season (\d{1,2})$')
    for name in os.listdir(base_path):
        full_path = os.path.join(base_path, name)
        if os.path.isdir(full_path):
            match = season_folder_pattern.match(name)
            if match:
                season_num = int(match.group(1))
                if use_leading_zero:
                    padded_name = f"Season {season_num:02}"
                else:
                    padded_name = f"Season {season_num}"
                new_path = os.path.join(base_path, padded_name)
                if full_path != new_path and not os.path.exists(new_path):
                    os.rename(full_path, new_path)
                    inherit_permissions(new_path, base_path)
                    print(f"🔄 Renamed '{name}' → '{padded_name}'")

def create_season_folders(base_path, seasons, use_leading_zero):
    for season in seasons:
        season_num = season.get("season_number")
        if season_num == 0:
            continue
        if use_leading_zero:
            folder_name = f"Season {season_num:02}"
        else:
            folder_name = f"Season {season_num}"
        folder_path = os.path.join(base_path, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            inherit_permissions(folder_path, base_path)
            print(f"📁 Created: {folder_name}")
        else:
            print(f"✔️ Folder exists: {folder_name}")

def move_files_to_seasons(base_path, use_leading_zero):
    for filename in os.listdir(base_path):
        full_path = os.path.join(base_path, filename)
        if os.path.isfile(full_path):
            match = SEASON_EPISODE_PATTERN.search(filename)
            if match:
                season_num = int(match.group(1))
                if use_leading_zero:
                    dest_folder = os.path.join(base_path, f"Season {season_num:02}")
                else:
                    dest_folder = os.path.join(base_path, f"Season {season_num}")
                if os.path.exists(dest_folder):
                    print(f"📂 Moving '{filename}' → '{dest_folder}'")
                    shutil.move(full_path, dest_folder)
                else:
                    print(f"⚠️ Season folder '{dest_folder}' not found. Skipping '{filename}'")
            else:
                print(f"⏭️ No SxxExx pattern in '{filename}'")

def process_all_show_folders(root_path, use_leading_zero, api_key):
    for folder_name in os.listdir(root_path):
        match = FOLDER_PATTERN.match(folder_name)
        if not match:
            continue

        show_name, year = match.groups()
        folder_path = os.path.join(root_path, folder_name)
        if not os.path.isdir(folder_path):
            continue

        print(f"\n📺 Processing: {show_name} ({year})")

        rename_unpadded_season_folders(folder_path, use_leading_zero)

        show = get_tmdb_show(api_key, show_name, year)
        if not show:
            continue

        seasons = get_seasons(api_key, show["id"])
        if not seasons:
            print("🚫 No seasons found.")
            continue

        valid_seasons = [s['season_number'] for s in seasons if s['season_number'] != 0]
        print(f"📊 Seasons found: {valid_seasons}")

        create_season_folders(folder_path, seasons, use_leading_zero)
        move_files_to_seasons(folder_path, use_leading_zero)

    print("\n✅ All done!")

if __name__ == "__main__":
    api_key, use_leading_zero = load_api_key_and_format()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    process_all_show_folders(current_dir, use_leading_zero, api_key)
