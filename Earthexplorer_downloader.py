import PySimpleGUI as sg
import landsatxplore.api
from landsatxplore.earthexplorer import EarthExplorer
import traceback

#PySimpleGUI theme
sg.theme('Dark')
#calendar font
fnt = 'Arial 12'
#empty list to display the found data
names = []

#window Content
layout = [
#login section
        [sg.Text("Username:"), sg.Input(key='-USER-')], [sg.Text('Password:'), sg.Input(key='-PW-', password_char='♥')],
        [sg.Button('Login', button_color=('white', 'black'), key='-LOGIN-')],
#scene parameter section
        [sg.Text(text='', size=(40, 1), key='-OUTPUT-')],
        [sg.Text('Satellite:', pad=((3, 0), 0)), sg.OptionMenu(values=('landsat_tm_c1', 'landsat_tm_c2_l1', 'landsat_tm_c2_l2',
                                                                       'landsat_etm_c1', 'landsat_etm_c2_l1', 'landsat_etm_c2_l2',
                                                                       'landsat_8_c1', 'landsat_ot_c2_l1', 'landsat_ot_c2_l2', 'sentinel_2a'), size=(20, 1), key='-SAT-')],
        [sg.Text('Latitude:'), sg.Input(key='-LAT-')],
        [sg.Text('Longitude:'), sg.Input(key='-LON-')],
        [sg.Text('Cloud-Cover in %:', pad=((3, 0), 0)), sg.OptionMenu(values=('10', '20', '30', '40', '50', '60', '70', '80', '90', '100'), size=(20, 1), key='-CC-')],
        [sg.In(key='-S_CAL-', enable_events=True, visible=True), sg.Col([[sg.CalendarButton('Select start date', target='-S_CAL-', key='-CAL_S-', font=fnt, format=('%Y-%m-%d'))]]),
         sg.In(key='-E_CAL-', enable_events=True, visible=True), sg.Col([[sg.CalendarButton('Select end date', target='-E_CAL-', key='-CAL_E-', font=fnt, format=('%Y-%m-%d'))]])],
        [sg.Text(size=(40, 1), key='-SCENES-')],
        [sg.Button('Start', button_color=('white', 'black'), key='-START-'), sg.Button('Reset', button_color=('white', 'firebrick3'), key='-RESET-')],
#download section
        [sg.Listbox(names, size=(60, 4), enable_events=True, key='-LIST-')],
        [sg.InputText(key='-SAVE_TXT-', enable_events=True, default_text='Enter Path here', size=(50, 4)), sg.FileSaveAs(button_text='Choose Folder', key='-SAVE-', initial_folder='/tmp')],
        [sg.ProgressBar(max_value=100, size=(30, 10), key='-BAR-')],
        [sg.Button('Download', button_color=('white', 'red'), key='-DOWN-')]]

#window layout
window = sg.Window("Earthexploder downloader", layout,
                   default_element_size=(12, 1),
                   text_justification='r',
                   auto_size_text=False,
                   auto_size_buttons=False,
                   default_button_element_size=(12, 1),
                   resizable=True,
                   finalize=True)


for key, state in {'-LOGIN-': False, '-START-': True, '-RESET-': True, '-DOWN-': True}.items():
    window[key].update(disabled=state)
recording = have_data = False

while True:
    event, values = window.read()
    print(event)
    if event == sg.WIN_CLOSED:
        break
#login button event
    if event == '-LOGIN-':
        for key, state in {'-LOGIN-': True, '-START-': False, '-RESET-': False, '-DOWN-': True}.items():
            window[key].update(disabled=state)
        username = values['-USER-']
        password = values['-PW-']
        try:
            api = landsatxplore.api.API(username, password)
            window['-OUTPUT-'].update('Hello ' + values['-USER-'] + '! Welcome to the Earthexplorer downloader!')
        except:
            window['-OUTPUT-'].update('Login failed! Please press Reset.')
        recording = True
#start button event
    elif event == '-START-':
        for key, state in {'-LOGIN-': True, '-START-': True, '-RESET-': False, '-DOWN-': False}.items():
            window[key].update(disabled=state)
        scenes = api.search(
            dataset=values['-SAT-'],
            latitude=float(values['-LAT-']),
            longitude=float(values['-LON-']),
            bbox=None,
            max_cloud_cover=values['-CC-'],
            start_date=values['-S_CAL-'],
            end_date=values['-E_CAL-'],
            months=None)
        window['-SCENES-'].update('{} scenes found.'.format(len(scenes)))
        for scene in scenes:
            names.append(scene['display_id'])
        window['-LIST-'].update(names)
        recording = True
#reset button event
    elif event == '-RESET-':
        [window[key].update(disabled=value) for key, value in {'-LOGIN-': False, '-START-': False, '-RESET-': True, '-DOWN-': True}.items()]
        recording = False
        have_data = False
#download button event
    elif event == '-DOWN-' and len(values['-LIST-']):
        for key, state in {'-LOGIN-': True, '-START-': True, '-RESET-': False, '-DOWN-': False}.items():
            window[key].update(disabled=state)
        x = values['-LIST-']
        username = values['-USER-']
        password = values['-PW-']
        ## Something wrong with EElandsatxplore --help
        ee = EarthExplorer(username, password)
        #Download Progress Bar
        progress = 0
        step = 1
        download = ee.download(x[0], output_dir=values['-SAVE_TXT-'])
        window['-BAR-'].update_bar(download)
        download += step
        ee.logout()

window.close()
