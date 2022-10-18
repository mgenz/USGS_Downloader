import landsatxplore.api
import sys

username = 'mgenz'
password = 'jcdfSdCUMFg9'

# Initialize a new API instance and get an access key
api = landsatxplore.api.API(username, password)

print("Welcome to the NDVI-Downloader! Would you like to continue?")

choice = ''

    # Give all the choices in a series of print statements.
print("\nPress Y to continue.")
print("Press N to close the Program.")

choice = input("\nWhat would you like to do? ")

# Respond to the user's choice.
if choice == 'y':
    print("\nSuccess\n")
elif choice == 'n':
    print("\nSee you later.\n")
    sys.exit()
else:
    print("\nI don't understand that choice, please try again.\n")
    sys.exit()

##Getting Data
dataset = 'LANDSAT_8_C1'

while True:
    latitude=float(input("Please enter a valid latitude: "))
    if latitude > 90:
        print("There is no such latitude!")
        continue
    elif latitude < -90:
        print("There is no such latitude!")
        continue
    else:
        break

while True:
    longitude=float(input("Please enter a valid Longitude: "))
    if longitude > 180:
        print("There is no such longitude!")
        continue
    elif longitude < -180:
        print("There is no such longitude!")
        continue
    else:
        break

bbox= None

while True:
    max_cloud_cover=float(input("Please enter the maximum cloud cover in percent: "))
    if max_cloud_cover > 100:
        print("The maximum cloud cover can't be over 100%!")
        continue
    elif max_cloud_cover < 0:
        print("The maximum cloud cover can't be less than 0%!")
        continue
    else:
        break

'''while True:
    start_date=float(input("Please enter the maximum cloud cover in percent: "))
    if start_date > 100:
        print("The maximum cloud cover can't be over 100%!")
        continue
    elif longitude < 0:
        print("The maximum cloud cover can't be less than 0%!")
        continue
    else:
        break
'''

start_date = '2021-01-01'
end_date = '2021-03-01'

# Request
scenes = api.search(
    dataset,
    latitude,
    longitude,
    bbox,
    max_cloud_cover,
    start_date,
    end_date,
    months=None,
    max_results=20)


print('{} scenes found.'.format(len(scenes)))

for scene in scenes:
    print('Scene ID:', scene['displayId'], ',Date:', scene['acquisitionDate'])

api.logout()