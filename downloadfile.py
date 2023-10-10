from pathlib import Path
import requests
from tqdm import tqdm
import zipfile
import os
import getopt
import sys
import gzip
import shutil

class DownloadFile(object):

    def __init__(self):
        pass
        
       
    @staticmethod
    def download(url, *, file_name='', folder_name='Data', overwrite=False, duplicate=False, progress_bar=True):
        
        if overwrite and duplicate:
            raise BaseException("Overwrite and duplicate arguments cannot be true simlutaneously!")

        if not file_name:
            file_name = url.split('/')[-1][:-4]
        
        # Set Folder path
        folder_path = Path(f'./{folder_name}/')
        file_name_with_postfix = f"{file_name}.{url.split('/')[-1].split('.')[-1]}"
        file_path = folder_path / file_name_with_postfix

        if folder_path.is_dir():
            print(f'----- > Folder "./{folder_name}" already exists')
        else:
            print(f'----- > Folder "./{folder_name}"  not found....')
            print(f'----- > creating "./{folder_name}"')
            folder_path.mkdir(parents=True, exist_ok=True)

        
        flag = ''
        
        if file_path.exists():
            currents = [entry.name for entry in os.scandir(folder_path) if entry.name[0:len(file_name)] == file_path.stem]
            flag = len(currents)
        
        file_postfix = url.split('/')[-1].split('.')[-1]
        
        if not flag=='': 
            
            if duplicate:
                print(f'----- > File "./{file_path}" already exists...making duplicates')
                file_path = folder_path / f'{file_name}({flag}).{file_postfix}'
                print(f'----- > New file : "./{file_path}"')
                DownloadFile.download_from_url_(url, file_path, progress_bar=progress_bar)
            elif overwrite:
                print(f'----- > "{file_path}" already exists....removing the current one and overwrite the new one')
                os.remove(file_path)
                DownloadFile.download_from_url_(url, file_path, progress_bar=progress_bar)
            else:
                print(f'----- > File "{file_path}" already exsists')
        else:
            DownloadFile.download_from_url_(url, file_path, progress_bar=progress_bar)
            
    
    @staticmethod
    def unzip(file_path, *, keep_zip=True):
        folder_path = Path(f'{file_path.parent}/{file_path.stem}')
        if not folder_path.exists():
            print(f'----- > file "./{file_path.parent}/{file_path.stem}" does not exists!')
            print(f'----- > Extracting file "./{file_path}" to "./{file_path.parent}/{file_path.stem}"... ')
            
            os.mkdir(folder_path) 
        
            with zipfile.ZipFile(file_path, 'r') as f_2:
                f_2.extractall(folder_path)
            print(f'----- > Completed.')
            if not keep_zip:
                print(f' ---- > Removing "{file_path}"...')
                os.remove(file_path)

        else:
            print(f'----- > file "./{file_path.parent}/{file_path.stem}" already exists!')
    
    @staticmethod
    def download_from_url_(url, file_path, progress_bar=True):
        if progress_bar:
            with open(file_path, 'wb') as f:
                        print('----- > Downloading the file...')
                        with requests.get(url, stream=True) as r:
                            r.raise_for_status()
                            total = int(r.headers.get('content-length', 0))
                        
                            tqdm_params = {
                                    
                                    'total': total,
                                    'miniters': 1,
                                    'unit': 'B',
                                    'unit_scale': True,
                                    'unit_divisor': 1024,
                                }
                            with tqdm(**tqdm_params) as pb:
                                for chunk in r.iter_content(chunk_size=8192):
                                    pb.update(len(chunk))
                                    f.write(chunk)
                        print(f'----- > Completed!')
                        print(f'----- > New File saved at ./{file_path}')
        else:
            with open(file_path, 'wb') as f:
                print("Downloading the file...")
                req = requests.get(url)
                f.write(req.content)
        
    @staticmethod
    def unzip_gz(file_path, *, keep_original=True):
        file_path = Path(file_path)
        new_path = Path(f'{file_path.parent}/{file_path.stem}')
        if not new_path.exists():
            print(f'----- > file "./{file_path.parent}/{file_path.stem}" does not exists!')
            print(f'----- > Extracting file "./{file_path}" to "./{file_path.parent}/{file_path.stem}"... ')
            
             

            with gzip.open(file_path, 'rb') as f_in:
                with open(new_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            if not keep_original:
                print(f' ---- > Removing "{file_path}"...')
                os.remove(file_path)
            
            
        
                
if __name__ == '__main__':
    
    help = "Please provide flags in this format:\n [-h] | [-u <url> -f <folder_name>  -d -o] | [-uz <file_path>] | [-ug <file_path>]\
    \n [-h or --help: Show help]\
    \n [-u or --url : URL which you can download your file from\
    \n -f or --folder_name: folder name to which the downloaded file will be stored\
    \n -d or --duplicate: if passed, in case the file already exists, new one with counting() will be downloaded and saved\
    \n -o or --overwrite: if passed, in case the file already exists, new one will be overwritten on the current one]\
    \n [-u or --unzip: unzip the ordinary zip file]\
    \n [-g or --unzipgz: unzip gz file]\
    "
    
    try:
      
        opts, _ = getopt.getopt(sys.argv[1:], 'hu:f:u:g:do', ['help','url', 'folder', 'unzip', 'unzipgz', 'duplicate', 'overwrite'])
      
    except:
        print('Unexpected flag!')
        print(help)
        sys.exit(2)
    folder_name = 'Data'
    url = None
    duplicate = False
    overwrite = False
    zip_path = False
    zip_gz_path = False
    print(opts)
    for opt, arg in opts:
        
        if opt in ('-u', '--url'):
            url = arg
        elif opt in ('-f', '--folder'):
            folder_name = arg
        elif opt in ('-d', '--duplicate'):
            duplicate = True
        elif opt in ('-o', '--overwrite'):
            overwrite = True
        elif opt in ('-u', '--unzip'):
            zip_path = arg
        elif opt in ('-g', '--unzipgz'):
            zip_gz_path = arg
        elif opt in ('-h', '--help'):
            print(help)
            sys.exit()

            

    if (overwrite and duplicate):
        print('Both overwrite and duplicate cannot be true!')
        sys.exit(2) 
    
    if zip_path:
        DownloadFile.unzip(zip_path)
    
        
    if zip_gz_path:
        DownloadFile.unzip_gz(zip_gz_path)
    
    
    try:
        DownloadFile.download(url, folder_name=folder_name, duplicate=duplicate, overwrite=overwrite)
    except:
        pass