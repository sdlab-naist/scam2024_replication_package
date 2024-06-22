# scam2024_replication_package

This is the replication package for producing the results of RQ4.

This will output the distribution of eight metrics for the year before and the year after DPP adoption.
- #Tags
- #Supported images
- #Architectures
- #All commits
- #Dockerfile commits
- #Bug-fixes
- #Releases
- #End of support

Please run the scripts in the following order:
```
research_dpp_timing.py
research_commit_hash.py
clone_metadata.py
research-BdppAdpp.py
collect_proj_character.py
analyze_meta.py
violin_plot.py
```
The graphs for the eight results will be output to the ``./figure`` folder.
