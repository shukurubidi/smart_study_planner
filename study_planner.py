import os

DATA_FILE = "study_log.txt"

def classify_session(duration):
    """Classifies a session duration into 'Short', 'Medium', or 'Long'."""
    if duration < 30:
        return "Short"
    elif 30 <= duration <= 90:
        return "Medium"
    else:
        return "Long"

def load_sessions():
    """Loads existing study sessions from the text file on startup."""
    sessions = []
    if not os.path.exists(DATA_FILE):
        return sessions
    try:
        with open(DATA_FILE, "r") as file:
            for line in file:
                parts = line.strip().split("|")
                if len(parts) == 4:
                    subject, topic, date_label, duration = parts
                    sessions.append({
                        "subject": subject,
                        "topic": topic,
                        "date": date_label,
                        "duration": int(duration)
                    })
    except Exception as e:
        print(f"Error loading data: {e}")
    return sessions

def save_sessions(sessions):
    """Saves all logged study sessions to the text file."""
    try:
        with open(DATA_FILE, "w") as file:
            for session in sessions:
                line = f"{session['subject']}|{session['topic']}|{session['date']}|{session['duration']}\n"
                file.write(line)
    except Exception as e:
        print(f"Error saving data: {e}")

def add_session(sessions):
    """Prompts user for session details, validates duration, and adds to list."""
    print("\n--- Add a Study Session ---")
    subject = input("Enter subject name: ").strip()
    topic = input("Enter topic covered: ").strip()
    date_label = input("Enter date or day label (e.g., Mon, 2026-09-07): ").strip()
    
    while True:
        try:
            duration = int(input("Enter duration in minutes (positive number): "))
            if duration > 0:
                break
            print("Duration must be greater than 0. Try again.")
        except ValueError:
            print("Invalid input. Please enter a valid integer for minutes.")
            
    session = {
        "subject": subject,
        "topic": topic,
        "date": date_label,
        "duration": duration
    }
    sessions.append(session)
    print("Study session added successfully!")

def view_sessions(sessions):
    """Displays every logged session in a neatly formatted table."""
    print("\n--- All Study Sessions ---")
    if not sessions:
        print("No study sessions recorded yet.")
        return

    print(f"{'Index':<6} | {'Subject':<15} | {'Topic':<20} | {'Date/Day':<12} | {'Duration (min)':<14} | {'Classification':<15}")
    print("-" * 92)
    
    for idx, s in enumerate(sessions, 1):
        classification = classify_session(s['duration'])
        print(f"{idx:<6} | {s['subject']:<15} | {s['topic']:<20} | {s['date']:<12} | {s['duration']:<14} | {classification:<15}")

def search_by_subject(sessions):
    """Searches and displays sessions matching a subject name (case-insensitive)."""
    print("\n--- Search Sessions by Subject ---")
    if not sessions:
        print("No study sessions recorded yet.")
        return
        
    query = input("Enter subject name to search: ").strip().lower()
    matched = [s for s in sessions if s['subject'].lower() == query]
    
    if not matched:
        print(f"No sessions found for subject '{query}'.")
        return
        
    total_minutes = sum(s['duration'] for s in matched)
    total_hours = total_minutes / 60
    
    print(f"\nFound {len(matched)} session(s) for '{query}':")
    print(f"{'Subject':<15} | {'Topic':<20} | {'Date/Day':<12} | {'Duration (min)':<14} | {'Classification':<15}")
    print("-" * 85)
    
    for s in matched:
        classification = classify_session(s['duration'])
        print(f"{s['subject']:<15} | {s['topic']:<20} | {s['date']:<12} | {s['duration']:<14} | {classification:<15}")
        
    print(f"\nTotal time spent on '{query}': {total_minutes} minutes ({total_hours:.2f} hours)")

def study_statistics(sessions):
    """Computes and displays overall and per-subject statistics."""
    print("\n--- Study Statistics ---")
    if not sessions:
        print("No study sessions recorded yet to compute statistics.")
        return
        
    total_overall_mins = sum(s['duration'] for s in sessions)
    print(f"Total hours studied overall: {total_overall_mins / 60:.2f} hours ({total_overall_mins} mins)")
    
    subject_totals = {}
    for s in sessions:
        subj = s['subject']
        subject_totals[subj] = subject_totals.get(subj, 0) + s['duration']
        
    print("\nTotal hours studied per subject:")
    for subj, mins in subject_totals.items():
        print(f"  - {subj}: {mins / 60:.2f} hours ({mins} mins)")
        
    weakest_subject = min(subject_totals, key=subject_totals.get)
    print(f"\nSubject with the least total study time (Weakest Area): {weakest_subject} ({subject_totals[weakest_subject]} mins)")
    
    longest_session = max(sessions, key=lambda x: x['duration'])
    print(f"\nSingle longest session recorded:")
    print(f"  - Subject: {longest_session['subject']}")
    print(f"  - Topic: {longest_session['topic']}")
    print(f"  - Duration: {longest_session['duration']} minutes ({classify_session(longest_session['duration'])} session)")
    print(f"  - Date/Day: {longest_session['date']}")

def main():
    """Main function controlling the menu-driven console interface."""
    sessions = load_sessions()
    
    while True:
        print("\n==============================")
        print("    SMART STUDY PLANNER       ")
        print("==============================")
        print("1. Add a study session")
        print("2. View all sessions")
        print("3. Search sessions by subject")
        print("4. View statistics")
        print("5. Save and exit")
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == '1':
            add_session(sessions)
        elif choice == '2':
            view_sessions(sessions)
        elif choice == '3':
            search_by_subject(sessions)
        elif choice == '4':
            study_statistics(sessions)
        elif choice == '5':
            save_sessions(sessions)
            print("Sessions saved successfully. Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice! Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()
