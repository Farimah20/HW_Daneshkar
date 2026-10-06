# recommender.py
# Mini Recommendation System
# This program suggests movies based on the similarity of users' tastes

# For reading and writing JSON files
import json
# For checking file existence
import os

JSON_FILE = "users.json"

# Step 1: Load user data from JSON file or default dictionary

def load_users() -> dict:
    """
    Reads the users.json file if it exists.
    If the file does not exist, creates it with default data and returns the default dictionary.
    Output: dict -> {username: [movie_list]}
    """
    # Expanded default dataset with diverse users and movies for better recommendations
    default_users = {
        "Ali":     ["Inception", "The Matrix", "Interstellar", "The Dark Knight"],
        "Sara":    ["Titanic", "Inception", "La La Land", "The Notebook"],
        "Reza":    ["The Matrix", "Interstellar", "Inception", "Blade Runner 2049", "Arrival"],
        "Mina":    ["Titanic", "Interstellar", "Forrest Gump", "The Pursuit of Happyness"],
        "Dara":    ["The Dark Knight", "Inception", "The Prestige", "Memento", "Tenet"],
        "Lena":    ["La La Land", "Titanic", "Pride and Prejudice", "Amelie", "The Grand Budapest Hotel"],
        "Karim":   ["Blade Runner 2049", "The Matrix", "Ex Machina", "Her", "Arrival"],
        "Nadia":   ["Forrest Gump", "The Shawshank Redemption", "The Pursuit of Happyness", "Good Will Hunting"],
        "Omar":    ["The Dark Knight", "Joker", "Fight Club", "Se7en", "The Silence of the Lambs"],
        "Yasmin":  ["Amelie", "La La Land", "Eternal Sunshine of the Spotless Mind", "Before Sunrise"],
        "Cyrus":   ["Interstellar", "Arrival", "Contact", "2001: A Space Odyssey", "Gravity"],
        "Layla":   ["The Notebook", "Pride and Prejudice", "Sense and Sensibility", "Atonement"],
        "Tariq":   ["Joker", "Fight Club", "American History X", "Requiem for a Dream"],
        "Shirin":  ["The Grand Budapest Hotel", "Amelie", "Midnight in Paris", "Lost in Translation"],
        "Babak":   ["The Shawshank Redemption", "Good Will Hunting", "Dead Poets Society", "Rain Man"],
    }

    # If the file exists, read and return its contents
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        # File not found - create it automatically with default data
        print(f"\n  '{JSON_FILE}' not found. Creating it with default data...")
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(default_users, f, indent=4, ensure_ascii=False)
        print(f"  '{JSON_FILE}' created successfully with {len(default_users)} users.")
        return default_users

# Step 6: Save data to JSON file

def save_users(users: dict):
    """
    Saves the users dictionary to the users.json file.
    Parameter users: dictionary {username: [movie_list]}
    """
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)
    print(f"\n  User data saved to '{JSON_FILE}'.")

# Helper: Print a styled section header

def print_header(title: str):
    width = 54
    print("\n" + "=" * width)
    print(f"  {title}")
    print("=" * width)


def print_divider():
    print("-" * 54)

# Helper: Collect a validated, duplicate-free movie list from input

def collect_movies(prompt_label: str, min_count: int = 2, existing: list = None) -> list:
    """
    Repeatedly asks the user for a comma-separated list of movies.
    - Detects and reports duplicates within the input itself.
    - Detects and reports movies already in 'existing' list (for updates).
    - Re-prompts until a valid, duplicate-free list with at least min_count entries is provided.
    Output: clean list of unique movie titles, or [] if the user cancels.
    """
    existing_lower = set(m.lower() for m in (existing or []))

    while True:
        raw = input(f"  {prompt_label}: ").strip()

        # Allow the user to cancel input
        if raw.lower() in ("cancel", "exit", "q"):
            return []

        # Split and clean entries
        entries = [m.strip() for m in raw.split(",") if m.strip()]

        if not entries:
            print("  [!] No input detected. Please enter at least one movie title.")
            continue

        # Detect duplicates within the user's own input
        seen = {}
        for movie in entries:
            key = movie.lower()
            seen[key] = seen.get(key, 0) + 1

        inline_dupes = [m for m, count in seen.items() if count > 1]

        if inline_dupes:
            print(f"\n  [!] You entered the following title(s) more than once:")
            for d in inline_dupes:
                print(f"      - {d}")
            print("  Please re-enter your list without duplicates.\n")
            continue

        # Detect movies already in the existing list
        already_have = [m for m in entries if m.lower() in existing_lower]

        if already_have:
            print(f"\n  [!] The following title(s) are already in your list:")
            for m in already_have:
                print(f"      - {m}")
            # Keep only the genuinely new ones
            entries = [m for m in entries if m.lower() not in existing_lower]
            if not entries:
                print("  No new movies to add. Please enter different titles.\n")
                continue
            print(f"  Keeping {len(entries)} new title(s): {entries}\n")

        # Enforce minimum count
        if len(entries) < min_count:
            print(f"  [!] Please enter at least {min_count} movies. You provided {len(entries)}.\n")
            continue

        return entries

# Steps 2 & 3: Enter username / Create new user or update existing user

def get_or_create_user(name: str, users: dict) -> tuple[dict, bool]:
    """
    Checks whether the user already exists.
    - New user: collects favorite movies and registers them.
    - Existing user: presents an update menu.
    Output: (users_updated, changed)
    """
    changed = False

    if name not in users:
        print_header(f"NEW USER  --  {name}")
        print(f"  Hello {name}! You are not registered in the system.")
        print("  Please enter 2 or more of your favorite movies.")
        print("  Separate titles with commas.  Type 'cancel' to abort.\n")

        movies = collect_movies("Favorite movies", min_count=2)

        if not movies:
            print("  Registration cancelled.")
        else:
            users[name] = movies
            changed = True
            print(f"\n  Registered successfully with {len(movies)} movie(s):")
            for i, m in enumerate(movies, 1):
                print(f"    {i:>2}. {m}")
    else:
        print_header(f"WELCOME BACK  --  {name}")
        print(f"  Your current list ({len(users[name])} movie(s)):\n")
        for i, m in enumerate(users[name], 1):
            print(f"    {i:>2}. {m}")

        print_divider()
        print("  Would you like to update your list?")
        print("  [1]  Add new movies")
        print("  [2]  Remove a movie")
        print("  [3]  Replace entire list")
        print("  [4]  No changes  (continue)")
        print_divider()

        choice = input("  Select option [1-4]: ").strip()

        if choice == "1":
            # Add new movies
            print(f"\n  Enter movies to add. Type 'cancel' to go back.\n")
            new_movies = collect_movies("Movies to add", min_count=1, existing=users[name])
            if new_movies:
                users[name].extend(new_movies)
                changed = True
                print(f"\n  Added {len(new_movies)} movie(s). Updated list ({len(users[name])}):")
                for i, m in enumerate(users[name], 1):
                    print(f"    {i:>2}. {m}")

        elif choice == "2":
            # Remove a movie
            print(f"\n  Enter the number of the movie to remove:\n")
            for i, m in enumerate(users[name], 1):
                print(f"    {i:>2}. {m}")
            try:
                idx = int(input("\n  Movie number: ").strip()) - 1
                if 0 <= idx < len(users[name]):
                    removed = users[name].pop(idx)
                    changed = True
                    print(f"  Removed: '{removed}'")
                    if not users[name]:
                        print("  [!] Your list is now empty. Recommendation may not work.")
                else:
                    print("  [!] Invalid number. No changes made.")
            except ValueError:
                print("  [!] Invalid input. No changes made.")

        elif choice == "3":
            # Replace entire list
            print(f"\n  Enter your new list of movies (min 2). Type 'cancel' to abort.\n")
            new_list = collect_movies("New movie list", min_count=2)
            if new_list:
                users[name] = new_list
                changed = True
                print(f"\n  List replaced with {len(new_list)} movie(s):")
                for i, m in enumerate(users[name], 1):
                    print(f"    {i:>2}. {m}")

        else:
            print("  No changes made.")

    return users, changed

# Helper: Calculate the number of movies in common between two users

def similarity(user_a: list, user_b: list) -> int:
    set_a = set(m.lower() for m in user_a)
    set_b = set(m.lower() for m in user_b)
    return len(set_a & set_b)

# Step 4: Find the most similar user (best match)

def find_best_match(name: str, users: dict) -> tuple[str | None, int]:
    current_movies = users.get(name, [])
    best_match = None
    best_score = 0

    for other_name, other_movies in users.items():
        if other_name == name:
            continue
        score = similarity(current_movies, other_movies)
        if score > best_score or (score == best_score and score > 0 and other_name < (best_match or "")):
            best_score = score
            best_match = other_name

    return best_match, best_score

# Step 5: Recommend movies the current user has not seen yet

def recommend_for(name: str, users: dict):
    """
    Based on the best match, presents a recommendation menu
    with multiple options for how to view recommendations.
    """
    best_match, score = find_best_match(name, users)

    if best_match is None or score == 0:
        print("\n  No similar user found. Cannot make a recommendation.")
        return

    print_header("RECOMMENDATION")
    print(f"  Most similar user : {best_match}")
    print(f"  Movies in common  : {score}")
    print_divider()

    current_lower = set(m.lower() for m in users[name])
    match_movies  = users[best_match]

    # Build full unseen list
    unseen = [m for m in match_movies if m.lower() not in current_lower]

    # Also gather top unseen from ALL other users sorted by similarity
    all_unseen = {}
    for other_name, other_movies in users.items():
        if other_name == name:
            continue
        s = similarity(users[name], other_movies)
        for movie in other_movies:
            if movie.lower() not in current_lower:
                key = movie.lower()
                if key not in all_unseen or all_unseen[key][1] < s:
                    all_unseen[key] = (movie, s)

    ranked = sorted(all_unseen.values(), key=lambda x: -x[1])

    # Recommendation menu
    print("  Choose how you would like to receive recommendations:\n")
    print("  [1]  Top recommendation from best match")
    print("  [2]  All unseen movies from best match")
    print("  [3]  Top 5 recommendations across all users")
    print("  [4]  Top 10 recommendations across all users")
    print("  [5]  Show who else has similar taste")
    print("  [6]  Skip recommendation")
    print_divider()

    choice = input("  Select option [1-6]: ").strip()

    if choice == "1":
        if unseen:
            print(f"\n  Recommended for you  -->  {unseen[0]}")
        else:
            print(f"\n  {best_match} has no new movies to suggest.")

    elif choice == "2":
        if unseen:
            print(f"\n  All unseen movies from {best_match} ({len(unseen)}):\n")
            for i, m in enumerate(unseen, 1):
                print(f"    {i:>2}. {m}")
        else:
            print(f"\n  {best_match} has no new movies to suggest.")

    elif choice == "3":
        top = ranked[:5]
        if top:
            print(f"\n  Top 5 recommendations for you:\n")
            for i, (movie, s) in enumerate(top, 1):
                print(f"    {i}. {movie:<40} (match score: {s})")
        else:
            print("\n  No recommendations available.")

    elif choice == "4":
        top = ranked[:10]
        if top:
            print(f"\n  Top 10 recommendations for you:\n")
            for i, (movie, s) in enumerate(top, 1):
                print(f"    {i:>2}. {movie:<40} (match score: {s})")
        else:
            print("\n  No recommendations available.")

    elif choice == "5":
        print(f"\n  Users ranked by similarity to {name}:\n")
        scores = []
        for other_name, other_movies in users.items():
            if other_name == name:
                continue
            s = similarity(users[name], other_movies)
            if s > 0:
                scores.append((other_name, s))
        scores.sort(key=lambda x: -x[1])
        if scores:
            print(f"  {'User':<20} {'Movies in Common':>16}")
            print("  " + "-" * 38)
            for uname, s in scores:
                print(f"  {uname:<20} {s:>16}")
        else:
            print("  No users with matching taste found.")

    else:
        print("\n  Recommendation skipped.")

# Main function: Run the entire program

def main():
    print("\n" + "=" * 54)
    print("  MOVIE RECOMMENDATION SYSTEM")
    print("=" * 54)

    # Step 1: Load data
    users = load_users()
    print(f"\n  {len(users)} user(s) loaded from '{JSON_FILE}'.")

    # Step 2: Get username
    print_divider()
    name = input("\n  Enter your name: ").strip()

    if not name:
        print("  Invalid name. Exiting.")
        return

    # Step 3: Register or update user
    users, changed = get_or_create_user(name, users)

    if name not in users:
        return

    # Steps 4 & 5: Recommendation menu
    recommend_for(name, users)

    # Step 6: Save if changed
    if changed:
        save_users(users)

    print("\n" + "=" * 54)
    print("  Thank you for using the Movie Recommendation System.")
    print("=" * 54 + "\n")


# Run main function only when the file is executed directly
if __name__ == "__main__":
    main()
