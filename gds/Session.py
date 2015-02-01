__author__ = 'adrian'
import httplib2
from oauth2client.client import OAuth2WebServerFlow
from googleapiclient.discovery import build


class Session(object):
    def __init__(self):
        super(Session, self).__init__()
        self.CLIENT_ID = '623115825375-u7n2lt303muvj42jl7j5unj2c28566o9.apps.googleusercontent.com'

        self.CLIENT_SECRET = '5rBDhBm-dxPqmXypoTmyJcNl'
        # Check https://developers.google.com/drive/scopes for all available scopes
        self.OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'

        # Redirect URI for installed apps
        self.REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'
        self.HTTP = None


    def authorize(self):
        flow = OAuth2WebServerFlow(self.CLIENT_ID, self.CLIENT_SECRET, self.OAUTH_SCOPE,
                                   redirect_uri=self.REDIRECT_URI)
        authorize_url = flow.step1_get_authorize_url()
        print 'Go to the following link in your browser:\n' + authorize_url
        code = raw_input('Enter verification code: ').strip()
        credentials = flow.step2_exchange(code)

        # Create an httplib2.Http object and authorize it with our credentials
        http = httplib2.Http()
        http = credentials.authorize(http)
        self.HTTP = http


    def getService(self):
        if self.HTTP is None:
            self.authorize()
        drive_service = build('drive', 'v2', http=self.HTTP)
        return drive_service