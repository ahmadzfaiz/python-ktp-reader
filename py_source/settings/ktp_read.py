import os
import re
import easyocr
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