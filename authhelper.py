from urllib.parse import quote, urlencode

# Client ID and secret
client_id = 'cf9ae668-9606-4e3a-8544-c7bb1db69553'
client_secret = 'OzZpkfhqRMb2LhDWFtPgGXa'

# Constant strings for OAuth2 flow
# The OAuth authority
authority = 'https://login.microsoftonline.com'

# The authorize URL that initiates the OAuth2 client credential flow for admin consent
authorize_url = '{0}{1}'.format(authority, '/common/oauth2/v2.0/authorize?{0}')

# The token issuing endpoint
token_url = '{0}{1}'.format(authority, '/common/oauth2/v2.0/token')

# The scopes required by the app
scopes = [ 'openid',
           'https://outlook.office.com/mail.read',
           'https://outlook.office.com/calendar.readwrite' ]

def get_signin_url(redirect_uri):
  # Build the query parameters for the signin url
  params = { 'client_id': client_id,
             'redirect_uri': redirect_uri,
             'response_type': 'code',
             'scope': ' '.join(str(i) for i in scopes)
           }

  signin_url = authorize_url.format(urlencode(params))

  return signin_url