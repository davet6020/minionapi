select i.hostname,i.ip, ct.chk_key, s.run_secs from inventory i, chk_type ct, scheduler s where i.id = 1


This is the query that works
============================
select i.hostname, i.ip, s.cron, s.chk_id, ct.chk_key from inventory i join scheduler s on i.id=s.hostid join chk_type ct on s.chk_id=ct.chk_id where i.hostname = 'koda';

hostname         ip                  run_secs  chk_id  chk_key
---------------  ------------------  --------  ------  -------------------
koda             192.168.1.151       120       1       chk_uptime
koda             192.168.1.151       86400     2       chk_cpuhardware
koda             192.168.1.151       3600      3       chk_diskhardware
koda             192.168.1.151       60        4       chk_diskutilisation
koda             192.168.1.151       60        5       chk_memutilisation

