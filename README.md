TomsDockerfiles
===============

A personal collection of Dockerfile files that I use in my day to day
testing.  They work for me, but buyer beware!

I've also included an assortment of scripts that are used by these Dockerfiles.

**To Run**

- Clone this repository to your test machine.
- Copy the interesting Dockerfile.{toolname} as listed below to ./Dockerfile.  
- Build the image:
  - Note: {toolname} must be all lowercase for the docker commands.
  - docker build -t {toolname} .   #Note period at end
    - i.e. docker build -t hellofromcontainer .
- Create and run the container:
  - docker run {toolname}
  - Push the image to Docker Hub to save.  This will require a dockerhub.com account and that you login prior to issuing this command with 'docker login':
    - docker push {toolname}

**Tools** 

***CreateVolume***

This creates a small text file in the /mydata directory/volume in the container.  

To run this particular container:

# docker build -t test_volume .  
# docker run -it --rm test_volume sh
/ # ls -alF /mydata  

Last command should show 'hi.txt' in the /mydata directory.

Related files:
  * Dockerfile.CreateVolume

***HelloFromContainer***

This runs a small python script that prints out "Hello World from Container Land" a few times before stopping.  It's useful to see if python can run in the container and if output is viewable.  

Related files:  
  * Dockerfile.HelloFromContainer
  * HelloFromContainer.py 
  
***LsRoot***

This sets up Fedora in the container and then does a 'ls -alF' on the root directory.  It shows that Fedora is up and running in the container and that the file systems are working properly.  

Related files:  
  * Dockerfile.LsRoot

***RestMonitor***

A small website monitoring tool that uses REST API calls to ensure that the
websites as noted in the WebServerList.txt file are up and responsive.  
Configuration options are in RestMonitor.config to configure the pause time
between checks, the number of loops and an optional email to send information to.
The webservices that are checked in this code do not require authentication;
RestMonitor.py would need some small changes to make that work.

Related files:  
  * Dockerfile.RestMonitor
  * RestMonitor.py 
  * RestMonitor.config
  * WebServerList.txt

***WhaleSayFortune***

From Docker's getting started tutorial, this will print a whale with a fortune in it's blow.  This is useful to check the general container environment.

Related files:
  - Dockerfile.CowSayFortune
 

**Sample Output**

***HelloFromContainer***
```
# docker run hellofromcontainer
Hello World from Container Land! Message # [0]
Hello World from Container Land! Message # [1]
Hello World from Container Land! Message # [2]
Hello World from Container Land! Message # [3]
Hello World from Container Land! Message # [4]
Hello World from Container Land! Message # [5]
Hello World from Container Land! Message # [6]
Hello World from Container Land! Message # [7]
Hello World from Container Land! Message # [8]
Hello World from Container Land! Message # [9]
```
***LsRoot***
```
# docker run lsroot
total 0
drwxr-xr-x.   1 root root   6 May  9 17:44 ./
drwxr-xr-x.   1 root root   6 May  9 17:44 ../
-rwxr-xr-x.   1 root root   0 May  9 17:44 .dockerenv*
lrwxrwxrwx.   1 root root   7 Feb  3  2016 bin -> usr/bin/
dr-xr-xr-x.   2 root root   6 Feb  3  2016 boot/
drwxr-xr-x.   5 root root 340 May  9 17:44 dev/
drwxr-xr-x.   1 root root  66 May  9 17:44 etc/
drwxr-xr-x.   2 root root   6 Apr 20 23:23 home/
lrwxrwxrwx.   1 root root   7 Feb  3  2016 lib -> usr/lib/
lrwxrwxrwx.   1 root root   9 Feb  3  2016 lib64 -> usr/lib64/
drwx------.   2 root root   6 Apr 20 23:23 lost+found/
drwxr-xr-x.   2 root root   6 Feb  3  2016 media/
drwxr-xr-x.   2 root root   6 Feb  3  2016 mnt/
drwxr-xr-x.   2 root root   6 Feb  3  2016 opt/
dr-xr-xr-x. 119 root root   0 May  9 17:44 proc/
dr-xr-x---.   2 root root 137 Apr 20 23:23 root/
drwxr-xr-x.   2 root root   6 Apr 20 23:23 run/
lrwxrwxrwx.   1 root root   8 Feb  3  2016 sbin -> usr/sbin/
drwxr-xr-x.   2 root root   6 Feb  3  2016 srv/
dr-xr-xr-x.  13 root root   0 May  9 13:14 sys/
drwxrwxrwt.   7 root root 170 Apr 20 23:23 tmp/
drwxr-xr-x.  12 root root 144 Apr 20 23:23 usr/
drwxr-xr-x.  19 root root 249 Apr 20 23:23 var/
```
***RestMonitor***

```
# docker run restmonitor
Using this config file: RestMonitor.config

############
Reading Configuration File
############

Verifying Webserver []
Unable to send e-mail
URLError for webserver: 
Request Time: 0 seconds, Return Json: []


Verifying Webserver [query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22boston%2C%20ma%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys]
Unable to send e-mail
Request Time: 3.1143107414245605 seconds, Return Json: {"query": {"count": 1, "created": "2017-05-09T15:01:55Z", "lang": "en-US", "results": {"channel": {"units": {"distance": "mi", "pressure": "in", "speed": "mph", "temperature": "F"}, "title": "Yahoo! Weather - Boston, MA, US", "link": "http://us.rd.yahoo.com/dailynews/rss/weather/Country__Country/*https://weather.yahoo.com/country/state/city-2367105/", "description": "Yahoo! Weather for Boston, MA, US", "language": "en-us", "lastBuildDate": "Tue, 09 May 2017 11:01 AM EDT", "ttl": "60", "location": {"city": "Boston", "country": "United States", "region": " MA"}, "wind": {"chill": "50", "direction": "115", "speed": "7"}, "atmosphere": {"humidity": "52", "pressure": "1013.0", "rising": "0", "visibility": "16.1"}, "astronomy": {"sunrise": "5:30 am", "sunset": "7:52 pm"}, "image": {"title": "Yahoo! Weather", "width": "142", "height": "18", "link": "http://weather.yahoo.com", "url": "http://l.yimg.com/a/i/brand/purplelogo//uh/us/news-wea.gif"}, "item": {"title": "Conditions for Boston, MA, US at 10:00 AM EDT", "lat": "42.358631", "long": "-71.056702", "link": "http://us.rd.yahoo.com/dailynews/rss/weather/Country__Country/*https://weather.yahoo.com/country/state/city-2367105/", "pubDate": "Tue, 09 May 2017 10:00 AM EDT", "condition": {"code": "28", "date": "Tue, 09 May 2017 10:00 AM EDT", "temp": "51", "text": "Mostly Cloudy"}, "forecast": [{"code": "28", "date": "09 May 2017", "day": "Tue", "high": "53", "low": "42", "text": "Mostly Cloudy"}, {"code": "30", "date": "10 May 2017", "day": "Wed", "high": "57", "low": "45", "text": "Partly Cloudy"}, {"code": "28", "date": "11 May 2017", "day": "Thu", "high": "53", "low": "46", "text": "Mostly Cloudy"}, {"code": "28", "date": "12 May 2017", "day": "Fri", "high": "52", "low": "48", "text": "Mostly Cloudy"}, {"code": "39", "date": "13 May 2017", "day": "Sat", "high": "54", "low": "49", "text": "Scattered Showers"}, {"code": "39", "date": "14 May 2017", "day": "Sun", "high": "54", "low": "47", "text": "Scattered Showers"}, {"code": "39", "date": "15 May 2017", "day": "Mon", "high": "59", "low": "50", "text": "Scattered Showers"}, {"code": "30", "date": "16 May 2017", "day": "Tue", "high": "62", "low": "52", "text": "Partly Cloudy"}, {"code": "30", "date": "17 May 2017", "day": "Wed", "high": "63", "low": "52", "text": "Partly Cloudy"}, {"code": "30", "date": "18 May 2017", "day": "Thu", "high": "64", "low": "54", "text": "Partly Cloudy"}], "description": "<![CDATA[<img src=\"http://l.yimg.com/a/i/us/we/52/28.gif\"/>\n<BR />\n<b>Current Conditions:</b>\n<BR />Mostly Cloudy\n<BR />\n<BR />\n<b>Forecast:</b>\n<BR /> Tue - Mostly Cloudy. High: 53Low: 42\n<BR /> Wed - Partly Cloudy. High: 57Low: 45\n<BR /> Thu - Mostly Cloudy. High: 53Low: 46\n<BR /> Fri - Mostly Cloudy. High: 52Low: 48\n<BR /> Sat - Scattered Showers. High: 54Low: 49\n<BR />\n<BR />\n<a href=\"http://us.rd.yahoo.com/dailynews/rss/weather/Country__Country/*https://weather.yahoo.com/country/state/city-2367105/\">Full Forecast at Yahoo! Weather</a>\n<BR />\n<BR />\n(provided by <a href=\"http://www.weather.com\" >The Weather Channel</a>)\n<BR />\n]]>", "guid": {"isPermaLink": "false"}}}}}}


Verifying Webserver []
Unable to send e-mail
URLError for webserver: 
Request Time: 0 seconds, Return Json: []


Verifying Webserver [www.omdbapi.com/?t=Beauty+and+the+Beast&y=&plot=short&r=json]
Request Time: 1.0909059047698975 seconds, Return Json: {"Title": "Beauty and the Beast", "Year": "1991", "Rated": "G", "Released": "22 Nov 1991", "Runtime": "84 min", "Genre": "Animation, Family, Fantasy", "Director": "Gary Trousdale, Kirk Wise", "Writer": "Linda Woolverton (animation screenplay by), Brenda Chapman (story), Chris Sanders (story), Burny Mattinson (story), Kevin Harkey (story), Brian Pimental (story), Bruce Woodside (story), Joe Ranft (story), Tom Ellery (story), Kelly Asbury (story), Robert Lence (story)", "Actors": "Robby Benson, Jesse Corti, Rex Everhart, Angela Lansbury", "Plot": "A young woman whose father has been imprisoned by a terrifying beast offers herself in his place, unaware that her captor is actually a prince, physically altered by a magic spell.", "Language": "English, French", "Country": "USA", "Awards": "Won 2 Oscars. Another 25 wins & 21 nominations.", "Poster": "https://images-na.ssl-images-amazon.com/images/M/MV5BMzE5MDM1NDktY2I0OC00YWI5LTk2NzUtYjczNDczOWQxYjM0XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg", "Ratings": [{"Source": "Internet Movie Database", "Value": "8.0/10"}, {"Source": "Rotten Tomatoes", "Value": "93%"}, {"Source": "Metacritic", "Value": "95/100"}], "Metascore": "95", "imdbRating": "8.0", "imdbVotes": "329,892", "imdbID": "tt0101414", "Type": "movie", "DVD": "08 Oct 2002", "BoxOffice": "$47,611,331.00", "Production": "Buena Vista", "Website": "http://www.disney.com/beautyandthebeast", "Response": "True"}


Verifying Webserver []
Unable to send e-mail
URLError for webserver: 
Request Time: 0 seconds, Return Json: []


Verifying Webserver [www.notrealsite.com/api/?q=steak]
Unable to send e-mail
URLError for webserver: www.notrealsite.com/api/?q=steak
Request Time: 0 seconds, Return Json: []


Verifying Webserver []
Unable to send e-mail
URLError for webserver: 
Request Time: 0 seconds, Return Json: []


Verifying Webserver [en.wikipedia.org/w/api.php?action=query&titles=Albert_Einstein&prop=images&format=json]
Request Time: 0.40602970123291016 seconds, Return Json: {"continue": {"imcontinue": "736|Albert_Einstein_signature_1934.svg", "continue": "||"}, "query": {"normalized": [{"from": "Albert_Einstein", "to": "Albert Einstein"}], "pages": {"736": {"pageid": 736, "ns": 0, "title": "Albert Einstein", "images": [{"ns": 6, "title": "File:1919 eclipse positive.jpg"}, {"ns": 6, "title": "File:Albert Einstein's exam of maturity grades (color2).jpg"}, {"ns": 6, "title": "File:Albert Einstein (Nobel).png"}, {"ns": 6, "title": "File:Albert Einstein Head.jpg"}, {"ns": 6, "title": "File:Albert Einstein and Charlie Chaplin - 1931.jpg"}, {"ns": 6, "title": "File:Albert Einstein as a child.jpg"}, {"ns": 6, "title": "File:Albert Einstein at the age of three (1882).jpg"}, {"ns": 6, "title": "File:Albert Einstein german.ogg"}, {"ns": 6, "title": "File:Albert Einstein photo 1920.jpg"}, {"ns": 6, "title": "File:Albert Einstein photo 1921.jpg"}]}}}}


Sleeping for 60 seconds...
```

***WhaleSayFortune***
```
# docker run cowsayfortune
 ______________________ 
< Violence is molding. >
 ---------------------- 
    \
     \
      \     
                    ##        .            
              ## ## ##       ==            
           ## ## ## ##      ===            
       /""""""""""""""""___/ ===        
  ~~~ {~~ ~~~~ ~~~ ~~~~ ~~ ~ /  ===- ~~~   
       \______ o          __/            
        \    \        __/             
          \____\______/   

```

May 2017


