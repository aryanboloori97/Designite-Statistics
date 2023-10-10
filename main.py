from pathlib import Path
import downloadfile
import pandas as pd
import numpy as np
import subprocess
import requests
import os
import glob

df = pd.read_csv('Data/dataset.cs', dtype={'stars':str}, )




filtered_series = df.loc[df['language'] == 'Java', :]['repository'][:100]




def clone_repos(pandas_series, numbers=100):
    

    
    
    for item in filtered_series[1:numbers]:
        
        

        repo_path = Path(f'repos/{item.split("/")[0]}-{item.split("/")[1]}')
        
        if not repo_path.exists(): 
            subprocess.run(['git', 'clone', f'http://github.com/{item}', f'repos/{item.split("/")[0]}-{item.split("/")[1]}'])




def run_designite():
    for repo in os.scandir('repos'):
        subprocess.run(['java', '-jar', 'DesigniteJava.jar', '-i', f'./repos/{repo.name}', '-o', f'./results/{repo.name}'])




class Repo():
    
    
    def __init__(self, name:str):
        self.name = name
        self.arch_smells = {}
        self.des_smells = {}
        self.impl_smells = {}
        self.testab_smells = {}
        self.test_smells = {}
        
    




def produce_results():
    repos = [Repo(repo.name) for repo in os.scandir('repos')]
    main_types_of_smells = ['ArchitectureSmells', 'DesignSmells', 'ImplementationSmells', 'TestabilitySmells', 'TestSmells']
    general_info = {smell:{} for smell in main_types_of_smells}



    for repo in repos:
        for csv_file in glob.glob(f'results/{repo.name}/*Smells.csv'):
            smell_type = csv_file.split('/')[-1].split('.')[0]
            column_smell_category = f"{smell_type.split('S')[0]} S{smell_type.split('S')[1][:-1]}"
            df = pd.read_csv(csv_file, encoding='utf-8', on_bad_lines='skip')
            unique_categories = [df[colm].value_counts() for colm in df.columns if colm==column_smell_category][0].to_dict()
            
            if smell_type == 'ArchitectureSmells':
                repo.arch_smells.update(unique_categories)
                for type, amount in repo.arch_smells.items():
                    if general_info[smell_type].get(type):
                        general_info[smell_type][type] += amount
                    else:
                        general_info[smell_type][type] = 1
                        
            if smell_type == 'DesignSmells':
                repo.des_smells.update(unique_categories)
                
                for type, amount in repo.des_smells.items():
                    if general_info[smell_type].get(type):
                        general_info[smell_type][type] += amount           
                    else:
                        general_info[smell_type][type] = 1

            if smell_type == 'ImplementationSmells':
                repo.impl_smells.update(unique_categories)         
                for type, amount in repo.impl_smells.items():
                    if general_info[smell_type].get(type):
                        general_info[smell_type][type] += amount        
                    else:
                        general_info[smell_type][type]  = 1
            if smell_type == 'TestabilitySmells':
                repo.testab_smells.update(unique_categories)       
                for type, amount in repo.testab_smells.items():
                    if general_info[smell_type].get(type):
                        general_info[smell_type][type] += amount
                    else:
                        general_info[smell_type][type]  = 1        
            if smell_type == 'TestSmells':
                repo.test_smells.update(unique_categories)       
                for type, amount in repo.test_smells.items():
                    if general_info[smell_type].get(type):
                        general_info[smell_type][type] += amount
                    else:
                        general_info[smell_type][type] = 1
    return general_info, main_types_of_smells
            

    
    
    


if __name__ == '__main__':
    # clone_repos(filtered_series)
    # run_designite()   
    result, smell_types = produce_results()
    
    with open('final_result.txt', 'w') as f:
        for smell in smell_types[-1::-1]:
            f.write(f'------------{smell}-------------\n')
            for key, value in result[smell].items():
                f.write(f'{key}:{value}')
                f.write('\n')