The objective of this program is to produce some statistical and analytical results regarding smells in different Java repositories.

The process of detecting and counting the smells is done by DesigniteJava tool.

This program just sorts and automates the process, not exploting any thing from the repos.

Everything is automated, so you should not download and put anything here by hand.
For the sake of convenience, I have also put DesigniteJave here(Not a professional action), so no need to do anything in this respect.

Step 1:

Use this command to download the dataset consisting the repos with names and language:

`python downloadfile.py -u https://reporeapers.github.io/static/downloads/dataset.csv.gz`

The dataset will be placed in `Data` folder with gz format.

Step 2:

then decompress it by this command:

`python downloadfile.py -g Data/dataset.cs.gz`
The .cs file will be placed in `Data` folder and now can be used by pandas.

Step 3:
Run this command to clone the java datasets. The default is the first 100 repos, but the item 1 (NCIP/c3pr-docs) is excluded due to being so bulky. The repos will be downloaded in `repos` folder. Some repos are not available so they will be skipped.
`python main.py`

Step 4:
Your result is ready on `final_result.txt` file.

Dependencies:

Just Pandas, all versions are almost ok.

NOTE**\*\*** : After running `main.py` if a github asked you username just click enter and skip it. Some repos are maybe private.
