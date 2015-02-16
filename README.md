# Flickrwall

<h2>Flickrwall</h2>

This is a collection of PIG scripts that deal with internal and external source in order to retrieve additional information abotu the landing page, such as Page Rank, Financial Ranking Score, etc.

The scripts are not dependent among them, therefore feel free to use the one that fits your need.

Edit the scripts in order to change the input path of the Creative Ids and the output path of the data you want to extract.

------------
<h3>Retrieve PageRank Score for a Domain URL</h3>

This script extract the PageRank score for a list of URL domains using the `WebCrawlCache` (WCC) on `Nitro-Blue`. 
For more information about the `WCC` visit [this twiki](http://twiki.corp.yahoo.com/view/Yst/WebCrawlCache).

<h4>Paths and Variables Required</h4>
* Input Domain List Path (single column with a domain per line)
* Last Dump Date, by default is 20141108 (it's not clear if there are new ones)
* Output Path

<h4>Example of Execution</h4>
Note that the PageRank dump in WCC is done monthly, but not all the time it is stored in the HCatalog. Therefore check the existence of that specific dump before chanking the value in the code, or just use the one specified in this code.
```
pig -useHCatalog extract-pagerank-domain.pig
```

<h4>Output Format</h4>
It is a simple file with two tab-separated columns that stand for:
```
domain <tab> domain_rank_list
http://horse.com/ <tab> {(48529)}
```
