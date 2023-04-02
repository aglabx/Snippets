#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 10.03.2023
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com

import requests
import re
from bs4 import BeautifulSoup

def get_ensembl_files(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href.endswith('/'):
            taxon = href[:-1]
            links.append((taxon, url + href))
    
    files_to_download = []
    for taxon, link in links:
        print(f"Getting files for {taxon}...")
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')
        for folder_link in soup.find_all('a'):
            folder_link = link + folder_link.get('href')
            if folder_link.endswith('/'):
                response = requests.get(folder_link)
                folder_soup = BeautifulSoup(response.content, 'html.parser')
                gz_files = []
                for file_link in folder_soup.find_all('a'):
                    file_href = file_link.get('href')
                    if file_href.endswith('.gz'):
                        gz_files.append(folder_link+file_href)
                        print((taxon, folder_link+file_href))
                files_to_download.append((taxon, link, gz_files))
    
    return files_to_download

  
def save_ensembl_files_tsv(files_to_download, output_file):
    with open(output_file, "w") as f:
        f.write("Taxon\tFilename\n")
        for taxon, link, gz_files in files_to_download:
            print(taxon, len(gz_files))
            for gz_file in gz_files:
                f.write(f"{taxon}\t{gz_file}\n")
    
    print("File saved successfully.")
    
if __name__ == '__main__':
  
    url = "https://ftp.ensembl.org/pub/release-106/fasta/"
    output_file = "ensembl_files.tsv"
    threads = 40
    work_folder = "/media/eternus1/nfs/projects/databases/ensembl_genomes"
    
    links = get_ensembl_files(url)
    save_ensembl_files_tsv(links, output_file)
    print("Please run bash commads:")
    print(f'''cd {work_folder}

# Create directories for each taxon
cut -f1 ensembl_files.tsv | uniq | xargs mkdir

# Download files for each taxon to the appropriate directory in 40 threads
cat ensembl_files.tsv | parallel -j {threads} --colsep '\t' 'echo "Downloading {2} for {1}..."; wget -P {1} {2}'''')
