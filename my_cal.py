import PySimpleGUI as sg

window = sg.Window('test', layout=[[sg.ProgressBar(max_value=100, size=(30,10), key='bar')]])

progress = 0
step = 5

while True:
	window.read(timeout=100)
	window['bar'].update_bar(progress)
	progress += step

	if progress > 100 or progress < 0:
		step *= -1