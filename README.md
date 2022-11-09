# get_species_taxids

```
git clone https://github.com/fo40225/get_species_taxids.git
cd get_species_taxids
pip install -r requirements.txt

wget https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz
tar axvf taxdump.tar.gz
python build_tree.py

# Staphylococcaceae
# Streptococcaceae
cat input.txt
90964
1300

python get_species_taxids.py -t input.txt > output.txt

# Streptococcus sp. BCCDCPHL-Ssp028
# Staphylococcus sp. HM-66
# ...
head output.txt
2070836
1572835
1444729
339641
1113956
269290
936580
1362620
2830759
423345

python get_species_taxids.py -t output.txt --level family
90964
1300
```