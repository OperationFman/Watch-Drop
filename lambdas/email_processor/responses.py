def get_add_success_content(tmdb_id):
    subject = f"Watch Drop: 💧 Subscription Added"
    body_text = f"You are now subscribed to episode updates for ID: {tmdb_id}."
    body_html = f"<html><body><p>You are now subscribed to episode updates for ID: <b>{tmdb_id}</b>.</p></body></html>"
    return subject, body_html, body_text

def get_nuke_confirmation_content(items_nuked):
    subject = f"Watch Drop: 🩸 Account Nuke Confirmation"
    body_text = f"Your Watch Drop account and {items_nuked} associated subscriptions have been successfully removed."
    body_html = f"<html><body><p>Your Watch Drop account and <b>{items_nuked}</b> associated subscriptions have been successfully removed.</p></body></html>"
    return subject, body_html, body_text

def get_command_not_understood_content(subject_lower):
    subject = "Watch Drop: 🩸 Command Not Understood"
    body_text = f"We couldn't understand your command: '{subject_lower}'. Please use 'add <TMDB_URL>', 'remove <TMDB_URL>', or 'nuke account'."
    body_html = f"<html><body><p>We couldn't understand your command: <b>'{subject_lower}'</b>.</p><p>Please use 'add &lt;TMDB_URL&gt;', 'remove &lt;TMDB_URL&gt;', or 'nuke account'.</p></body></html>"
    return subject, body_html, body_text

def get_invalid_tmdb_url_content(url_part):
    subject = f"Watch Drop: 🩸 Invalid TMDB URL"
    body_text = f"We couldn't parse a valid TMDB URL from your request: '{url_part}'. Please ensure it's a full TMDB URL."
    body_html = f"<html><body><p>We couldn't parse a valid TMDB URL from your request: <b>'{url_part}'</b>.</p><p>Please ensure it's a full TMDB URL (e.g., https://www.themoviedb.org/tv/123-show-name).</p></body></html>"
    return subject, body_html, body_text

def get_unsupported_content_type_content(content_type):
    subject = "Watch Drop: 🩸 Only TV Shows Supported"
    body_text = f"You requested '{content_type}' content, but only TV shows are currently supported. Please provide a TV show URL."
    body_html = f"<html><body><p>You requested <b>'{content_type}'</b> content, but only TV shows are currently supported.</p><p>Please provide a TV show URL.</p></body></html>"
    return subject, body_html, body_text

def get_remove_success_content(tmdb_id):
    subject = f"Watch Drop: 🩸 Subscription Removed"
    body_text = f"You are no longer subscribed to updates for TMDB TV show ID: {tmdb_id}."
    body_html = f"<html><body><p>You are no longer subscribed to updates for TMDB TV show ID: <b>{tmdb_id}</b>.</p></body></html>"
    return subject, body_html, body_text

def get_operation_failed_content(command_info, error_details):
    subject = "Watch Drop: 🩸 Operation Failed"
    body_text = f"An error occurred while processing your request '{command_info}'. Please try again. Error details: {error_details}"
    body_html = f"<html><body><p>An error occurred while processing your request <b>'{command_info}'</b>. Please try again.</p><p>Error details: {error_details}</p></body></html>"
    return subject, body_html, body_text

def get_help_instructions_content():
    subject = "Watch Drop: 💧 How to"
    body_text = """
    Here's how to use our email-driven TV show notification service:

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
        <h1 style="margin-bottom: 5px;">Hey 👋 Meet Watch Drop</h1>
        <p style="margin-bottom: 0;">Interested in using this email-driven TV show notification service?</p>
        <p style="margin-top: 0; margin-bottom: 20px;">Here's how</p>

        <img src="https://raw.githubusercontent.com/OperationFman/Watch-Drop/refs/heads/main/misc/WatchDropInstruction.png" alt="Watch Drop Instructions" style="max-width:60%;height:auto;display:block;margin: 0 20px">

        <div style="margin-bottom: 15px;">
            <h3 style="margin-bottom: 5px;">1. Find Your TV Show</h3>
            <p style="margin-top: 0;">Go to <a href="https://www.themoviedb.org/">The Movie Database</a> and search for the TV show you want notifications for</p>
        </div>

        <div style="margin-bottom: 15px;">
            <h3 style="margin-bottom: 5px;">2. Copy the Link</h3>
        </div>

        <div style="margin-bottom: 50px;">
            <h3 style="margin-bottom: 5px;">3. Send an Email</h3>
            <p style="margin-top: 0; margin-bottom: 0;">Recipient:</p>
            <b style="margin-left: 2px;"><code>subscribe@watchdrop.org</code></b>
            <p style="margin-bottom: 0; margin-top: 3px;">Subject:</p>
            <b style="margin-left: 2px;"><code>add https://www.themoviedb.org/tv/123-show-name</code></b>
            <p style="margin-top: 3px;">Send</p>
        </div>

        <div style="margin-bottom: 50px;">
            <h3 style="margin-bottom: 0;">Other Commands</h3>
            <p style="margin-top: 0; margin-bottom: 0;">Unsubscribe from a show:</p>
            <b style="margin-left: 2px;"><code>remove https://www.themoviedb.org/tv/123-show-name</code></b>

            <p style="margin-top: 15px; margin-bottom: 0;">Unsubscribe from everything (Delete account):</p>
            <b style="margin-left: 2px;"><code>nuke account</code></b> 

            <p style="margin-top: 15px; margin-bottom: 0;">Get Help:</p>
            <b><code>help</code></b> 
        </div>

        <p>That's it! Now just wait for a new episode to air</p>
        <p>Your notifications will look like this:</p>

        <img src="https://raw.githubusercontent.com/OperationFman/Watch-Drop/refs/heads/main/misc/WatchDropExample.png" alt="Watch Drop Example" style="max-width:100%;height:auto;display:block;margin:0 auto 20px auto;">

    </body>
    </html>
    """
    return subject, body_html, body_text