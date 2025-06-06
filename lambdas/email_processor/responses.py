def get_add_success_content(tmdb_id):
    subject = f"Watch Drop: Subscription Added"
    body_text = f"You are now subscribed to episode updates for ID: {tmdb_id}."
    body_html = f"<html><body><p>You are now subscribed TV show ID: <b>{tmdb_id}</b>.</p></body></html>"
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