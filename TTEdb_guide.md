I want to create a database of target trial emulation studies. I am right now conducting a meta-research study on the concordance between target trial emulations and their target trials. You can find the protocol in this .md file: Protocol_TTE_MetaResearch.md. Also, the extracted data for this meta-research study is in the dataset folder: dataset/TTE_Metaresearch_Clean_Dataset - Studies characteristics.csv for study characteristics and dataset/TTE_Metaresearch_Clean_Dataset - PICOs.csv for the PICO questions and the estimates from TTE and target RCT for that PICO.

I want to create a web app named TTEdb. This is a part of Xera DB. Xera DB projects use a same theme and a same structure. You can find the specifics of the theme and the structure in this folder: ~/Documents/Github/xeradb/shared_theme. The specifics for TTEdb are in css/themes/ttedb-theme.css. You can find the structure of other projects in ~/Documents/Github/OpenScienceTracker for OST project, ~/Documents/GitHub/CitingRetracted for PRCT project, and ~/Documents/GitHub/CIHRPT for CIHRPT project. Read each one carefully to understand the structure.

The structure of TTEdb is as follows:

- Main page: Shows the useful summary of the database and guide for the user.
- TTE page: Shows all TTE studies in the database. User can search in the database (just like the search page in PRCT project).
- TTE vs. RCT page: Shows the studies that have emulated an existing RCT which is exactly the thing that we are doing in the meta-research study. User can search in the database.
- Learning Hub page: Shows the learning hub for the user. This includes all the methodological papers that are relevant to the TTE project. Also, other relevant resources for TTE that include causal inference, directed acyclic graphs (DAGs), quantitative bias analysis (QBA), etc (add based on your knowledge).
- Statistics page: Shows the statistics of the database. This part should have two tabs: 
    - TTE vs. RCT: Shows the statistics of the TTE vs. RCT studies.
    - TTE: Shows the statistics of the other TTE studies.
Use everything that we have collected in the meta-research study to create the statistics. Use protocol and both CSV files to create the statistics.
- About page: Shows the about page for the user. This includes the team members, the funding, the license, etc. This page also should have contact part.

Also, all TTEs should have a page that shows the all details of the TTE, as illustrated in the both CSV files (use all of the information in the CSV files).

Then, 