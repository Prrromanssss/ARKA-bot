import os

from dotenv import load_dotenv

load_dotenv()

BOT_API_TOKEN = os.environ.get('BOT_API_TOKEN', 'summy-dummy-token')

SITE_URL = 'http://arka-pechi.ru/'

STOVE_URL = 'https://t.me/+8xk3vH5YSuoxOWMy'

BARBECUE_URL = 'https://t.me/+NhMVJp9xHSo2NDdi'

CHANNEL_URL = 'https://t.me/arka_pechi'

chat_to_poll = {
                'sourr_cream': os.environ.get(
                    'CHAT_ID_ADMIN_SOURR_CREAM',
                    '123456789'
                    ),
                }

DB_URI = 'dbsqlite3.db'

ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'summy-dummy-password')

CONTENT_TYPES = [
    'text', 'audio', 'document', 'photo',
    'sticker', 'video', 'video_note', 'voice',
    'location', 'contact', 'venue'
    ]
