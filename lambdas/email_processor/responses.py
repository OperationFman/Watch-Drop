def get_add_success_content(tmdb_id):
    subject = f"Watch Drop: Subscription Added"
    body_text = f"You are now subscribed to episode updates for ID: {tmdb_id}."
    body_html = f"<html><body><p>You are now subscribed to episode updates for ID: <b>{tmdb_id}</b>.</p></body></html>"
    return subject, body_html, body_text

def get_nuke_confirmation_content(items_nuked):
    subject = f"Watch Drop: Account Nuke Confirmation"
    body_text = f"Your Watch Drop account and {items_nuked} associated subscriptions have been successfully removed."
    body_html = f"<html><body><p>Your Watch Drop account and <b>{items_nuked}</b> associated subscriptions have been successfully removed.</p></body></html>"
    return subject, body_html, body_text

def get_command_not_understood_content(subject_lower):
    subject = "Watch Drop: Command Not Understood"
    body_text = f"We couldn't understand your command: '{subject_lower}'. Please use 'add <TMDB_URL>', 'remove <TMDB_URL>', or 'nuke account'."
    body_html = f"<html><body><p>We couldn't understand your command: <b>'{subject_lower}'</b>.</p><p>Please use 'add &lt;TMDB_URL&gt;', 'remove &lt;TMDB_URL&gt;', or 'nuke account'.</p></body></html>"
    return subject, body_html, body_text

def get_invalid_tmdb_url_content(url_part):
    subject = f"Watch Drop: Invalid TMDB URL"
    body_text = f"We couldn't parse a valid TMDB URL from your request: '{url_part}'. Please ensure it's a full TMDB URL."
    body_html = f"<html><body><p>We couldn't parse a valid TMDB URL from your request: <b>'{url_part}'</b>.</p><p>Please ensure it's a full TMDB URL (e.g., https://www.themoviedb.org/tv/123-show-name).</p></body></html>"
    return subject, body_html, body_text

def get_unsupported_content_type_content(content_type):
    subject = "Watch Drop: Only TV Shows Supported"
    body_text = f"You requested '{content_type}' content, but only TV shows are currently supported. Please provide a TV show URL."
    body_html = f"<html><body><p>You requested <b>'{content_type}'</b> content, but only TV shows are currently supported.</p><p>Please provide a TV show URL.</p></body></html>"
    return subject, body_html, body_text

def get_remove_success_content(tmdb_id):
    subject = f"Watch Drop: Subscription Removed"
    body_text = f"You are no longer subscribed to updates for TMDB TV show ID: {tmdb_id}."
    body_html = f"<html><body><p>You are no longer subscribed to updates for TMDB TV show ID: <b>{tmdb_id}</b>.</p></body></html>"
    return subject, body_html, body_text

def get_operation_failed_content(command_info, error_details):
    subject = "Watch Drop: Operation Failed"
    body_text = f"An error occurred while processing your request '{command_info}'. Please try again. Error details: {error_details}"
    body_html = f"<html><body><p>An error occurred while processing your request <b>'{command_info}'</b>. Please try again.</p><p>Error details: {error_details}</p></body></html>"
    return subject, body_html, body_text

def get_help_instructions_content():
    subject = "Watch Drop: How to"
    body_text = """
    Welcome to Watch Drop! Here's how to use our email-driven TV show notification service:

    1. Find Your TV Show:
       Go to The Movie Database (TMDB) at themoviedb.org and search for the TV show you want updates for.

    2. Copy the Link:
       For example: https://www.themoviedb.org/tv/123-show-name

    3. Subscribe to a Show:
       add [PASTE_YOUR_TMDB_LINK_HERE]

    4. Unsubscribe from a Show:
       remove [PASTE_YOUR_TMDB_LINK_HERE]

    5. Unsubscribe from Everything (Nuke Account):
       nuke account

    That's it! Enjoy staying updated on your favorite TV shows with Watch Drop.
    """
    body_html = """
    <html>
    <body>
        <p>Hello there. Here's how to use this email-driven TV show notification service:</p>
        <br/>
        
        <img src="https://d3atatnx15erez.cloudfront.net/WatchDropDemo.gif" alt="Watch Drop Demo" style="max-width:70%;height:auto;display:block;margin:0 auto;">
        <br/>
        

        <h3>1. Find Your TV Show</h3>
        <p>Go to <a href="https://www.themoviedb.org/">The Movie Database (TMDB)</a> and search for the TV show you want updates for.</p>
        <br/>       

        <h3>2. Copy the Link</h3>
        <p>Example:</p>
        <b><code>https://www.themoviedb.org/tv/123-show-name</code></b>
        <br/>

        <h3>3. Subscribe to a show</h3>
        <b><code>add [PASTE_YOUR_TMDB_LINK_HERE]</code></b> 
        <br/>

        <h3>4. Unsubscribe from a show</h3>
        <b><code>remove [PASTE_YOUR_TMDB_LINK_HERE]</code></b>
        <br/>        

        <h3>5. Unsubscribe from everything (Delete account)</h3>
        <b><code>nuke account</code></b>
        <br/>
        <br/>        

        <p>That's it! Enjoy staying updated on your favorite TV shows with Watch Drop.</p>
    </body>
    </html>
    """
    return subject, body_html, body_text