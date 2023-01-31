# import requests

# url = "https://netpacklogistic.com/api/measurement-entries"

# payload={'name': 'SMNP-2022-008'}

# files=[
#   ('file',('data.xlsx',open('data.xlsx','rb'),'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')),
#   ('image',('caliResult2.png',open('caliResult2.png','rb'),'image/png'))
# ]

# headers = {
#   'name': 'SMNP-2022-005',
#   'file': ''
# }

# response = requests.request("POST", url, headers=headers, data=payload, files=files)

# print(response.text)


# import requests

# url = "https://netpacklogistic.com/api/measurement-entries"

# payload={'name': 'FFNP-2022-005'}
# files=[
#   ('file',('data.xlsx',open('data.xlsx','rb'),'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')),
#   ('image',('caliResult1.png',open('caliResult1.png','rb'),'image/png'))
# ]
# headers = {}

# response = requests.request("POST", url, headers=headers, data=payload, files=files)

# print(response.text)

#length,breadth,height,weight,photo



# import requests

# url = "https://netpacklogistic.com/api/measurement-entries"

# payload={'name': 'SMNP-2022-006'}
# files=[
#   ('file',('data.xlsx',open('D:\DMS\data.xlsx','rb'),'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')),
#   ('image',('caliResult1.png',open('D:\DMS\caliResult1.png','rb'),'image/jpeg'))
# ]
# headers = {}

# response = requests.request("POST", url, headers=headers, data=payload, files=files)

# print(response.text)


#length.........breadth.......height.......weight......image .......shipping name .....box number

# import requests

# Name = 'ABCD-2023-006'
# Excel_Location = "D:/DMS/Dimensions/ABCD/1/ABCD-2023-005.xlsx"
# Excel_Name = "ABCD-2023-005.xlsx"
# # Excel_Location = "D:/DMS/Dimensions/SMNP/2/SMNP-2023-111.xlsx"
# # Excel_Name = "SMNP-2023-111.xlsx"
# # Photo_Location ="D:/DMS/Snapshots/ABCD/10/ABCD-2023-010/1.jpg"
# # Photo_Name = "1.jpg"
# # Name = "PPPP-2023-5"
# # Excel_Location = "D:/DMS/Dimensions/PPPP/2/PPPP-2023-5.xlsx"
# # Excel_Name = "PPPP-2023-5.xlsx"
# Photo_Location = "D:/DMS/Snapshots/PPPP-2023-5/PPPP-2023-5-2-9.jpg"
# Photo_Name = "PPPP-2023-5-2-9.jpg"

# url = "https://netpacklogistic.com/api/measurement-entries"

# payload={'name': Name}
# files=[
#   ('file',(Excel_Name,open(Excel_Location,'rb'),'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')),
#   ('image',(Photo_Name,open(Photo_Location,'rb'),'image/jpeg'))
# ]
# # files=[
# #   ('file',('ABCD-2023-010.xlsx',open('Dimensions/ABCD/10/ABCD-2023-010.xlsx','rb'),'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')),
# #   ('image',('1.jpg',open('Snapshots/ABCD/10/ABCD-2023-010/1.jpg','rb'),'image/jpeg'))
# # ]
# headers = {}

# response = requests.request("POST", url, headers=headers, data=payload, files=files)

# print(response.text)


# import requests

# url = "https://netpacklogistic.com/api/measurement-entries"

# payload={}
# files=[
#   ('file',('ABCD-2023-4.xlsx',open('Dimensions/ABCD/3/ABCD-2023-4.xlsx','rb'),'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')),
#   ('image',('SMNP-2023-1-1-2.jpg',open('Snapshots/SMNP-2023-1/SMNP-2023-1-1-2.jpg','rb'),'image/jpeg'))
# ]

# headers = {
#   'Accept': 'application/json',
#   'Cookie': 'XSRF-TOKEN=eyJpdiI6ImpodXl2T3VTRGNKWWl1MXhJRU01QWc9PSIsInZhbHVlIjoiS2hlajlKeEpDSldMNnpyYWE2NEtCR3N0bkxIK3dnMEVjNUVteGxoMlBzUUQ1Sk1ic3JGOURGcjBSTWRRMUN1ckZkdVFJWFBoNGdYVTRFRmRLaVN4NU84Z2g1TSsyT3dkREptbDdLNEpPZ0hXTmQweml5UGJHcVlIVU9oeVBydUoiLCJtYWMiOiIyZTQxZjJlNmNkYzA5ZjkwNWRkYTAxY2Y2NzdkZDA0MGM2ZmI3Y2ViYjA2OThhMzAzNThjYzI2NDE5ZjVhMTE3IiwidGFnIjoiIn0%3D; netpacklogistic_session=eyJpdiI6IndmQyt5ZTM2V0Fwemo2aVU4aU9TU1E9PSIsInZhbHVlIjoidTNNTmhxZFNPemh5RjRtNE8zNHRSNDR0WDFMWTJNak9yM2xxS1FpY3dBWVRrRmFKV2Vic05kclBUMnFjWHNQamRLVTFvTnZVT2FjQUJvMjhoOFE5cFRjWFpOOEJZZHVLVVZFVjlxdE1HR3ZEbjlQT21PRzFHcTRNK2hFcmlMMHIiLCJtYWMiOiIxYWQ2NzBmYWEzNTE5Zjk2YjE3NjJiYzIzZWYwOGFhZWQzZDI3M2FkMjFkMGQ0MWQ5NDlkYjgyNjQ5MDNjZmJmIiwidGFnIjoiIn0%3D'
# }

# response = requests.request("POST", url, headers=headers, data=payload, files=files)

# print(response.text)


import requests

url = "https://netpacklogistic.com/api/measurement-entries"

payload={}
files=[
  ('file',('TEST-2023-4.xlsx',open('D:/DMS/Dimensions/TEST/6/TEST-2023-4.xlsx','rb'),'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')),
  ('image',('SMNP-2023-1-1-2.jpg',open('D:/DMS/Snapshots/SMNP-2023-1/SMNP-2023-1-1-2.jpg','rb'),'image/jpeg'))
]
headers = {
  'Accept': 'application/json',
  # 'Cookie': 'XSRF-TOKEN=eyJpdiI6ImpodXl2T3VTRGNKWWl1MXhJRU01QWc9PSIsInZhbHVlIjoiS2hlajlKeEpDSldMNnpyYWE2NEtCR3N0bkxIK3dnMEVjNUVteGxoMlBzUUQ1Sk1ic3JGOURGcjBSTWRRMUN1ckZkdVFJWFBoNGdYVTRFRmRLaVN4NU84Z2g1TSsyT3dkREptbDdLNEpPZ0hXTmQweml5UGJHcVlIVU9oeVBydUoiLCJtYWMiOiIyZTQxZjJlNmNkYzA5ZjkwNWRkYTAxY2Y2NzdkZDA0MGM2ZmI3Y2ViYjA2OThhMzAzNThjYzI2NDE5ZjVhMTE3IiwidGFnIjoiIn0%3D; netpacklogistic_session=eyJpdiI6IndmQyt5ZTM2V0Fwemo2aVU4aU9TU1E9PSIsInZhbHVlIjoidTNNTmhxZFNPemh5RjRtNE8zNHRSNDR0WDFMWTJNak9yM2xxS1FpY3dBWVRrRmFKV2Vic05kclBUMnFjWHNQamRLVTFvTnZVT2FjQUJvMjhoOFE5cFRjWFpOOEJZZHVLVVZFVjlxdE1HR3ZEbjlQT21PRzFHcTRNK2hFcmlMMHIiLCJtYWMiOiIxYWQ2NzBmYWEzNTE5Zjk2YjE3NjJiYzIzZWYwOGFhZWQzZDI3M2FkMjFkMGQ0MWQ5NDlkYjgyNjQ5MDNjZmJmIiwidGFnIjoiIn0%3D'
}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

print(response.text)
