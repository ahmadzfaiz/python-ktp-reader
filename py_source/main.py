import os
import PySimpleGUI as sg
from .settings.ktp_read import ktp_image_read

def create_window(max_value, name_file):
  layout = [
    [sg.Text('Input Folder:', size=[10, 1]), sg.Input(key='input_folder', size=[50, 1]), sg.FolderBrowse(size=[10, 1])],
    [sg.Text('Output Folder:', size=[10, 1]), sg.Input(key='output_folder', size=[50, 1]), sg.FolderBrowse(size=[10, 1])],
    [sg.Column([], size=[20, 5])],
    [sg.ProgressBar(max_value, orientation='h', size=[42, 15], key='progressbar')],
    [sg.Text(name_file, key='data')],
    [sg.Exit(), sg.Button('Baca KTP')]
  ]
  return sg.Window("KTP Reader", layout, finalize=True)

window = create_window(100, '')

while True:
  event, values = window.read()

  # Define input files
  input_url = values['input_folder']
  input_files = [f'{input_url}/{file}' for file in os.listdir(input_url)]
  output_url = values['output_folder']

  if event in (sg.WINDOW_CLOSED, 'Exit'):
    break
  
  if event == 'Baca KTP':
    index = 0
    window = create_window(len(input_files), input_files[index])
    progress_bar = window['progressbar']
    progress_file = window['data']
    
    for data in input_files:
      progress_bar.UpdateBar(index+1)
      progress_file.update(input_files[index])
      window.refresh()
      ktp_image = ktp_image_read(data, output_url, input_files[index])
      index+=1
    sg.popup('Success')

window.close()