def new_ep_html(show_name, season_number, episode_number, episode_name, image_url, tmdb_url):
    return f"""
<html>
<body style="text-align: center;">
    <h1 style="text-align: center; margin-bottom: 30px;">💧</h1>
    <h2 style="text-align: center; margin: 0; padding: 0;">{show_name} - {episode_name}</h2>
    <h2 style="text-align: center;">Season {season_number} - Episode {episode_number}</h2>
    
    <p style="text-align: center;">Enjoy your Watch Drop!</p>
    <p style="text-align: center; margin-bottom: 50px;">Find more shows on <a href="https://www.themoviedb.org/">The Movie Database</a></p>

    <img src="{image_url}" alt="{show_name} Poster" style="max-width: 50%; height: auto; display: block; margin: 0 auto 50px;">
    
    <a href="mailto:subscribe@watchdrop.org?subject=remove%20{tmdb_url}" style="color: #FF5733;">Unsubscribe from this alert</a>
    <p></p>
    <a href="mailto:subscribe@watchdrop.org?subject=nuke%20account" style="color: #FF5733; font-weight: bold;">Unsubscribe ALL</a>
    
    <p>For support, email us at franklin.v.moon@gmail.com</p>
</body>
</html>
"""

def new_ep_text(show_name, season_number, episode_number, episode_name, tmdb_url):
    return f"""
{show_name} - {episode_name}
Season {season_number} - Episode {episode_number}

Enjoy your Watch Drop!
From the Watch Drop team

Unsubscribe from this alert: mailto:subscribe@watchdrop.org?subject=remove%20{tmdb_url}
Unsubscribe ALL: mailto:subscribe@watchdrop.org?subject=nuke%20account

For support, email us at franklin.v.moon@gmail.com
"""

