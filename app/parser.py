from flask_restx import reqparse

user_id_parser = reqparse.RequestParser()
user_id_parser.add_argument('id', type=int, required=True)

comment_parser = reqparse.RequestParser()
comment_parser.add_argument(
    'start_date',
    type=str,
    required=False,
    help='Start date in YYYY-MM-DD format')
comment_parser.add_argument(
    'end_date',
    type=str,
    required=False,
    help='End date in YYYY-MM-DD format')
comment_parser.add_argument(
    'sort_order',
    type=str,
    choices=[
        'asc',
        'desc'],
    default='asc',
    help='End date in YYYY-MM-DD format')
comment_parser.add_argument(
    'limit',
    type=int,
    default=10,
    required=False,
    help='Number of comments per page')
comment_parser.add_argument(
    'page',
    type=int,
    default=1,
    required=False,
    help='Page number to return')
