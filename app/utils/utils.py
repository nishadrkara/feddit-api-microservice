import requests
from datetime import datetime
from textblob import TextBlob
from config import Config
# fetch all user ids
# Constants for the API endpoint and headers
USER_DETAILS_URL = f"{Config.FEDDIT_KEY}subfeddits"
USER_COMMENTS_API_ENDPOINT = f'{Config.FEDDIT_KEY}comments/'
HEADERS = {'accept': 'application/json'}
DEFAULT_SKIP = 0
DEFAULT_LIMIT = 100


def fetch_data(
        url=USER_DETAILS_URL,
        headers=HEADERS,
        skip=DEFAULT_SKIP,
        limit=DEFAULT_LIMIT,
        **kwargs):
    """
    Fetch data from the API with pagination parameters.

    Args:
        url (str): The API endpoint URL.
        headers (dict): The headers to include in the request.
        skip (int): The number of items to skip for pagination.
        limit (int): The maximum number of items to return.

    Returns:
        dict: The JSON response from the API.
    """
    params = {'skip': skip, 'limit': limit, **kwargs}
    print(params)
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return {}


def extract_ids():
    """
    Extract IDs from the API response data.

    Args:
        data (dict): The JSON response data from the API.

    Returns:
        list: A list of extracted IDs.
    """
    data = fetch_data()
    return [subfeddit['id'] for subfeddit in data['subfeddits']]


def fetch_user_comments(user_id):
    """
    Fetch user comments for a given user ID.

    Args:
        user_id (str): The user ID to fetch comments for.

    Returns:
        list: A list of comments for the user.
    """

    skip = 0
    limit = 1000
    user_comments = []
    while True:
        data = fetch_data(
            url=USER_COMMENTS_API_ENDPOINT,
            skip=skip,
            limit=limit,
            subfeddit_id=user_id)
        comments = data.get('comments', [])
        user_comments.extend(comments)
        if len(comments) < limit:
            break
        skip += limit
    return user_comments


def convert_timestamp_to_datetime(timestamp):
    """
    Convert Unix timestamp to human-readable datetime format.

    Args:
        timestamp (int): The Unix timestamp.

    Returns:
        str: The formatted datetime string.
    """
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


def convert_str_to_date(timestamp):
    return datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S').date()


def analyze_comments(comments, start_time=None, end_time=None):
    """
    Analyze comments for sentiment polarity.

    Args:
        comments (list): A list of comments.

    Returns:
        list: A list of analyzed comments with sentiment polarity and score.
    """
    analyzed_comments = []
    for comment in comments:
        try:
            created_at = convert_timestamp_to_datetime(comment['created_at'])
            if start_time and end_time:
                if not (start_time <= convert_str_to_date(created_at) <= end_time):
                    continue
            username = comment['username']
            text = comment['text']
            polarity_score = TextBlob(text).sentiment.polarity
            polarity = 'positive' if polarity_score > 0 else 'negative' if polarity_score < 0 else 'neutral'

            analyzed_comments.append({
                'unique_identifier': comment['id'],
                'username': username,
                'text': text,
                'polarity': polarity,
                'polarity_score': polarity_score,
                'created_at': created_at
            })
        except Exception as e:
            print(e)
            raise ValueError(f"Error analyzing comment {comment}: {e}")
    return analyzed_comments


def all_user_comments(start_time=None, end_time=None, sort_order='asc'):
    all_user_comments = []
    all_user_ids = extract_ids()
    all_comments_analysis = []

    for user_id in all_user_ids:
        user_comments = fetch_user_comments(user_id)
        analyzed_comments = analyze_comments(user_comments, start_time, end_time)
        all_comments_analysis.extend(analyzed_comments)

    # check sort order
    reverse_order = True if sort_order == 'desc' else False
    all_comments_analysis.sort(key=lambda x: x['polarity_score'], reverse=reverse_order)
    return all_comments_analysis
