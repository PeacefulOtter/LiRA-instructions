
#  Overpass server instructions

### 1. SSH connection
(replace `<USER>` with your user name)
```console
$ ssh <USER>@lira-osm.compute.dtu.dk
``` 

### 2. Start the server
```console
user@lira-osm:~$ cd /opt/op/
user@lira-osm:/opt/op$ nohup bin/dispatcher --osm-base --db-dir=db --meta &
    & tail -f nohup.out
``` 
`tail -f nohup.out` will write the server logs to the `nohup.out` file 

<br/>

### Termine the server
```console
user@lira-osm:/opt/op$ bin/dispatcher --terminate`
``` 