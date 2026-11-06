import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# 🔑 CLIENT CREDENTIALS
CLIENT_ID = "5ef1f092cea9485f827675fa56b0fc88"
CLIENT_SECRET = "1ff76e1eb845468d8ac73ae00684d2ba"
PLAYLIST_ID = "YOUR_SECRET_KEY_HERE"
REDIRECT_URI = "http://127.0.0"


# 1. Connect to Spotify using the fixed numerical address
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="playlist-modify-public playlist-modify-private playlist-read-private"
))

def debug_playlist(playlist_id):
    print("🔄 Fetching your playlist tracks...")
    try:
        results = sp.playlist_items(playlist_id)
        tracks = results['items']
        
        while results['next']:
            results = sp.next(results)
            tracks.extend(results['items'])
            
        seen_track_ids = set()
        duplicate_uris = []
        
        print("🔍 Scanning for duplicate songs...")
        for item in tracks:
            if not item or 'track' not in item or not item['track']:
                continue
                
            track = item['track']
            track_id = track.get('id')
            track_name = track.get('name', 'Unknown Track')
            
            artists = track.get('artists')
            artist_name = artists[0].get('name', 'Unknown Artist') if artists else 'Unknown Artist'
            
            if not track_id:
                continue
                
            if track_id in seen_track_ids:
                print(f"❌ Found duplicate: {track_name} by {artist_name}")
                duplicate_uris.append(track['uri'])
            else:
                seen_track_ids.add(track_id)
                
        # 2. Delete the duplicates safely
        if duplicate_uris:
            print(f"🗑️ Removing {len(duplicate_uris)} duplicate tracks...")
            for i in range(0, len(duplicate_uris), 100):
                chunk = duplicate_uris[i:i+100]
                sp.playlist_remove_all_occurrences_of_items(playlist_id, chunk)
            print("🎉 Success! Your playlist has been debugged and cleaned.")
        else:
            print("✅ Your playlist is already perfectly clean! No duplicates found.")
    except Exception as e:
        print(f"⚠️ Error occurred: {e}")

if __name__ == "__main__":
    debug_playlist(PLAYLIST_ID)
