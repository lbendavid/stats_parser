# stats_parser

Some little script to analyse some data for usage statistics

## stat_juniper_log

Parse Juniper log to comute which device connect to company vpn 
and also user. Useful to stat how many people use vpn.

The juniper log is the `log.access`

## stat_plm_usage

Parse log of PLM launcher (3DExperience, Enovia V6, Catia V5) for 
each users and stat PLM 3D functions launch. Interestings to 
stat which users need GPU for its workstations.

## Typical use cases


```
$ cd ./stat_juniper_log
$ ./stat_juniper_log.sh -i var/log.access
[...code running...]
$
$ cd ..
$ cd ./stat_plm_usage
$ ./stat_plm_usage.sh
[...code running...]
```

# Why to store this scripts on Github ?

- To backup it
- To share some log parsing scripts in python and plot with
gnuplot

# Documentation used to do the scripts

- [Gnuplot Documentation](http://www.gnuplot.info/documentation.html)
- [Python3 Documentation](https://docs.python.org/3/)

# Todo list

- [] need a usage in bash
- [] need docstrings
- [] need tests??
- [] need to pass more variables to gnuplot or ==>
- [] leave gnuplot to matplotlib? [Matplotlib documentation](https://matplotlib.org/3.1.0/gallery/index.html)
