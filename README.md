# 3_bars

This script shows following information about bars from json file:
* which is the biggest
* which is the smallest
* which is closest to you

You can download the list of the bars [here](http://data.mos.ru/opendata/7710881420-bary).   
You can run the script using following command: _python bars.py \<path_to_json_file\>_

##Function of finding the closest bar 
This function uses modification of haversine formula
 witch can give very accurate distance in meters. 
 ![Folmula](http://wiki.gis-lab.info/images/8/89/Great-cirlcles-09.gif)
 
 You can find more information about haversine formula and its modification 
 [here](http://gis-lab.info/qa/great-circles.html) in **Russian**.  
 More info about haversine formula on [wiki](https://en.wikipedia.org/wiki/Haversine_formula) 
and [here](https://rosettacode.org/wiki/Haversine_formula) in **Engish** (no info about modifications).

There's **another formula** that finds distance between two points in Cartesian coordinates.  
It works properly if you want to find the closest bar in the city, but 
it is not very accurate and it cannot give information about actual distance.
What's more it would be incorrect on big distances. 

So I have chosen haversine formula, which is more complicated, but universal 
and more accurate.