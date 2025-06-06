def new_ep_html(show_name, season_number, episode_number, episode_name, image_url):
    return f"""
<html>
<body style="text-align: center;">
    <h1 style="text-align: center; margin-bottom: 30px;">💧</h1>
    <h2 style="text-align: center; margin: 0;">{show_name} - {episode_name}</h2>
    <h2 style="text-align: center;">Season {season_number} - Episode {episode_number}</h2>
    <img src="{image_url}" alt="{show_name} Poster" style="max-width: 50%; height: auto; display: block; margin: 0 auto 50px;">
    <p style="text-align: center;">Enjoy your Watch Drop!</p>
    <p style="text-align: center; margin-bottom: 20px;">From the Watch Drop team</p>
    <p>For support, email us at franklin.v.moon@gmail.com</p>
</body>
</html>
"""

def new_ep_text(show_name, season_number, episode_number, episode_name):
    return f"""
{show_name} - {episode_name}
Season {season_number} Episode {episode_number} 
has just aired. Enjoy your Watch Drop!
"""

