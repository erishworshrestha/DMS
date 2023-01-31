from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LoadCredentialsFile("mycreds.txt")
if gauth.credentials is None:
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    gauth.Refresh()
else:
    gauth.Authorize()

filename = 'data.csv'
gauth.SaveCredentialsFile("mycreds.txt")
drive = GoogleDrive(gauth)

file_list = drive.ListFile(
    {'q': "'root' in parents and trashed=false"}).GetList()
for file1 in file_list:
    if file1['title'] == filename:
        file1.Delete()

textfile = drive.CreateFile()
textfile.SetContentFile(filename)
textfile.Upload()