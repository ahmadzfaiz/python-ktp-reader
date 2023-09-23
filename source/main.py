import os
import re
import easyocr
import PySimpleGUI as sg
from datetime import datetime

def ktp_image_read(input, output, source):
  image_reader = easyocr.Reader(['id'], gpu=True)
  result = image_reader.readtext(input, detail=0)

  # Set log file
  log_path = f'{output}/log.txt'
  log_file = open(log_path, 'a')
  log_file.write(f"{str(datetime.now())} -- {','.join(result)}\n")
  
  def get_exact_attribute(data):
    return result[result.index(data)+1]
  
  def get_partial_attribute(data):
    substring = [item for item in result if data in item][0]
    return result[result.index(substring)+1]
  
  # Define empty data variable
  data = {}

  # Set nik
  try:
    data['nik'] = get_exact_attribute('NIK')
  except:
    data['nik'] = 'Gambar tidak terbaca'

  # Set nama
  try:
    data['nama'] = get_exact_attribute('Nama')
  except:
    data['nama'] = 'Gambar tidak terbaca'

  # Set lahir
  try:
    data_lahir = get_partial_attribute('Tgl')
  except:
    data_lahir = 'NONE 00-00-0000'

  try:
    data['tempat_lahir'] = re.findall("[A-Za-z]+", data_lahir)[0]
  except:
    data['tempat_lahir'] = 'Gambar tidak terbaca'

  try:
    data['tanggal_lahir'] = re.findall("[0-9-]+", data_lahir)[0]
  except:
    data['tanggal_lahir'] = 'Gambar tidak terbaca'

  # Set jenis_kelamin
  try:
    data['jenis_kelamin'] = get_partial_attribute('Jenis')
  except:
    data['jenis_kelamin'] = 'Gambar tidak terbaca'

  # Set pekerjaan
  try:
    data['pekerjaan'] = get_partial_attribute('kerja')
  except:
    data['pekerjaan'] = 'Gambar tidak terbaca'

  # Set data source
  data['data_source'] = source

  output_list = [
    data['nik'],
    data['nama'],
    data['tempat_lahir'],
    data['tanggal_lahir'],
    data['jenis_kelamin'],
    data['pekerjaan'],
    data['data_source']
  ]

  # Set output file
  output_path = f'{output}/output.csv'

  if os.path.isfile(output_path):
    output_file = open(output_path, 'a')
    output_file.write(','.join(output_list) + '\n')
  else:
    output_file = open(output_path, 'a')
    header = 'nik,nama,tempat_lahir,tanggal_lahir,jenis_kelamin,pekerjaan,data_source'
    output_file.write(f"{header}\n{','.join(output_list)}\n")

def create_window(max_value, name_file):
  layout = [
    [sg.Text('Input Folder:', size=[10, 1]), sg.Input(key='input_folder', size=[50, 1]), sg.FolderBrowse(size=[10, 1])],
    [sg.Text('Output Folder:', size=[10, 1]), sg.Input(key='output_folder', size=[50, 1]), sg.FolderBrowse(size=[10, 1])],
    [sg.Column([], size=[20, 5])],
    [sg.ProgressBar(max_value, orientation='h', size=[42, 15], key='progressbar')],
    [sg.Text(name_file, key='data')],
    [sg.Exit(), sg.Button('Verifikasi Input'), sg.Button('Baca KTP', disabled=True), sg.Button('Lisensi'), sg.Button('Tentang')]
  ]
  return sg.Window("KTP Reader", layout, finalize=True)

window = create_window(100, '')

while True:
  event, values = window.read()

  # Define input files
  input_url = values['input_folder']
  output_url = values['output_folder']

  if event in (sg.WINDOW_CLOSED, 'Exit'):
    break

  elif event == 'Verifikasi Input':
    if values['input_folder'] != '' and values['output_folder'] != '':
      sg.popup('Url valid')
      window['Baca KTP'].update(disabled=False)
    else:
      sg.popup('Url tidak valid')
      window['Baca KTP'].update(disabled=True)
  
  elif event == 'Baca KTP':
    input_files = [f'{input_url}/{file}' for file in os.listdir(input_url)]
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

  elif event == 'Lisensi':
    license = open("../LICENSE", 'r').read()
    content = f'''
      © 2023 Ahmad Zaenun Faiz
      {license}
    '''
    sg.popup_scrolled(content, title='Lisensi KTP Reader', size=[60, 10])

  elif event == 'Tentang':
    content = open("../docs/tentang.txt", 'r').read()
    sg.popup_scrolled(content, title='Tentang KTP Reader', size=[60, 10])

window.close()