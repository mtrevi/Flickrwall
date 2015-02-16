# Flickrwall

This python script will change your desktop wallpaper using your Flickr photos.
The script currently works only in Mac OSX.

------------
<h3>Configuration</h3>

The settins 

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
