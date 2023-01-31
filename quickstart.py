from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)

# file1 = drive.CreateFile({'title': ' test1.csv'})
# file1.SetContentString('Hello World! this is a second line')
# # file1.Upload()
# file1.SetContentString('Hello World! this is a third line')
# file1.Upload()


file_list = drive.ListFile(
    {'q': "'root' in parents and trashed=false"}).GetList()
for file1 in file_list:
    print('title: %s, id: %s' % (file1['title'], file1['id']))

# from pydrive.auth import GoogleAuth

# gauth = GoogleAuth()
# gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication.


# from pydrive.drive import GoogleDrive

# drive = GoogleDrive(gauth)

# # Create GoogleDriveFile instance with title 'Hello.txt'.
# file1 = drive.CreateFile({'title': 'Hello.txt'})
# # Set content of the file from given string.
# file1.SetContentString('Hello World!')
# file1.Upload()


gauth = GoogleAuth()
# Try to load saved client credentials
gauth.LoadCredentialsFile("mycreds.txt")
if gauth.credentials is None:
    # Authenticate if they're not there
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()
# Save the current credentials to a file
gauth.SaveCredentialsFile("mycreds.txt")

drive = GoogleDrive(gauth)

textfile = drive.CreateFile()
textfile.SetContentFile('eng.txt')
textfile.Upload()
print(textfile)

drive.CreateFile({'id': textfile['id']}).GetContentFile('eng-dl.txt')
