import base64
import json
import os

def read_and_decode_config(config_path):
    with open(config_path, 'r') as file:
        content = json.load(file)
    
    profiles_encoded = content.get('_profiles', '')
    try:
        decoded_profiles = json.loads(base64.b64decode(profiles_encoded))
        return content, decoded_profiles
    except Exception as e:
        print(f"Error decoding profiles: {e}")
        return content, {}

def encode_and_write_config(config_path, content, profiles):
    content['_profiles'] = base64.b64encode(json.dumps(profiles).encode()).decode()
    
    with open(config_path, 'w') as file:
        json.dump(content, file, indent=2)

def delete_profile(config_path):
    content, profiles = read_and_decode_config(config_path)
    
    if not profiles:
        print("No profiles found.")
        return
    
    print("Available profiles:")
    sorted_profiles = sorted(profiles.values(), key=lambda x: x['Name'])
    for i, profile in enumerate(sorted_profiles, 1):
        print(f"{i}. {profile['Name']} ({profile['NetworkProfile'].get('DomainName', 'No domain')})")
    
    try:
        choice = int(input("Enter the number of the profile to delete: ")) - 1
        
        if 0 <= choice < len(sorted_profiles):
            selected_profile = sorted_profiles[choice]
            profile_id = selected_profile['ID']
            
            # Remove from profiles dictionary
            del profiles[profile_id]
            
            # Remove the profile-specific entry
            profile_key = f"profile-{profile_id}"
            if profile_key in content:
                del content[profile_key]
            
            encode_and_write_config(config_path, content, profiles)
            print(f"Deleted profile: {selected_profile['Name']}")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Please enter a valid number.")

if __name__ == "__main__":
    config_path = os.path.expanduser('server-state.conf')
    
    if not os.path.exists(config_path):
        print("Configuration file not found.")
    else:
        delete_profile(config_path)
