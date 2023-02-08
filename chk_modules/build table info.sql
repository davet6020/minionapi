INSERT INTO scheduler (id, hostname, ip, chk_key, run_secs)
VALUES (1, 'koda', '192.168.1.151', 'chk_uptime', 120),
(2, 'samantha', '192.168.1.149', 'chk_uptime', 120),
(3, 'rizzo', '192.168.1.148', 'chk_uptime', 120),
(4, 'sofia', '192.168.1.150', 'chk_uptime', 120)

INSERT INTO scheduler (id, hostname, ip, chk_key, run_secs)
VALUES (5, 'koda', '192.168.1.151', 'chk_cpuhardware', 86400),
(6, 'samantha', '192.168.1.149', 'chk_cpuhardware', 86400),
(7, 'rizzo', '192.168.1.148', 'chk_cpuhardware', 86400),
(8, 'sofia', '192.168.1.150', 'chk_cpuhardware', 86400)

INSERT INTO scheduler (id, hostname, ip, chk_key, run_secs)
VALUES (9, 'koda', '192.168.1.151', 'chk_diskhardware', 3600),
(10, 'samantha', '192.168.1.149', 'chk_diskhardware', 3600),
(11, 'rizzo', '192.168.1.148', 'chk_diskhardware', 3600),
(12, 'sofia', '192.168.1.150', 'chk_diskhardware', 3600)

INSERT INTO scheduler (id, hostname, ip, chk_key, run_secs)
VALUES (13, 'koda', '192.168.1.151', 'chk_diskutilisation', 60),
(14, 'samantha', '192.168.1.149', 'chk_diskutilisation', 60),
(15, 'rizzo', '192.168.1.148', 'chk_diskutilisation', 60),
(16, 'sofia', '192.168.1.150', 'chk_diskutilisation', 60)

INSERT INTO scheduler (id, hostname, ip, chk_key, run_secs)
VALUES (17, 'koda', '192.168.1.151', 'chk_memutilisation', 60),
(18, 'samantha', '192.168.1.149', 'chk_memutilisation', 60),
(19, 'rizzo', '192.168.1.148', 'chk_memutilisation', 60),
(20, 'sofia', '192.168.1.150', 'chk_memutilisation', 60)


INSERT INTO inventory (id, hostname, ip)
VALUES(2, 'samantha', '192.168.1.149'),
(3, 'rizzo', '192.168.1.148'),
(4, 'sofia', '192.168.1.150')


INSERT INTO chk_type (id, chk_id, chk_key, chk_desc)
VALUES (1, '1', 'chk_uptime', 'How long the system has been running'),
 (2, '2', 'chk_cpuhardware', 'CPU specification; speed, manufacturer, etc'),
 (3, '3', 'chk_diskhardware', 'Disk mount points and device names'),
 (4, '4', 'chk_diskutilisation', 'Disk total size and free space'),
 (5, '5', 'chk_memutilisation', 'Memory total and memory free')


INSERT INTO scheduler (id, hostid, chk_id, cron)
VALUES (25, 1, 7, '1M'),
 (26, 2, 7, '1M'),
 (27, 3, 7, '1M'),
 (28, 4, 7, '1M');

INSERT INTO scheduler (hostid, chk_id, cron)
 (5, 2, '1D'),
 (5, 3, '1H'),
 (5, 4, '1M'),
 (5, 5, '1M'),
 (5, 6, '1D'),
 (5, 7, '1M');



CREATE TABLE `data_uptime` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hostid` int(11) NOT NULL,
  `chk_id` int(200) NOT NULL,
  `uptime` varchar(255) NOT NULL,
  `hostname` varchar(255) NOT NULL,
  `ip` varchar(255) NOT NULL,
  `date_recorded` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;


CREATE TABLE `data_cpuhardware` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hostid` int(11) NOT NULL,
  `chk_id` int(200) NOT NULL,
  `cpu_sockets` int(11) NOT NULL,
  `cpu_cores` int(11) NOT NULL,
  `model_name` varchar(255) NOT NULL,
  `cpu_mhz` varchar(255) NOT NULL,
  `hostname` varchar(255) NOT NULL,
  `ip` varchar(255) NOT NULL,
  `date_recorded` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;


CREATE TABLE `data_diskutilisation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hostid` int(11) NOT NULL,
  `chk_id` int(11) NOT NULL,
  `total_size` decimal(19,2) NOT NULL,
  `free_size` decimal(19,2) NOT NULL,
  `size_type` varchar(255) NOT NULL DEFAULT 'GB',
  `hostname` varchar(255) NOT NULL,
  `ip` varchar(255) NOT NULL,
  `date_recorded` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

CREATE TABLE `data_memutilisation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hostid` int(11) NOT NULL,
  `chk_id` int(11) NOT NULL,
  `memory_total` decimal(19,2) NOT NULL,
  `memory_free` decimal(19,2) NOT NULL,
  `size_type` varchar(255) NOT NULL DEFAULT 'GB',
  `hostname` varchar(255) NOT NULL,
  `ip` varchar(255) NOT NULL,
  `date_recorded` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

CREATE TABLE `data_cpuutilisation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hostid` int(11) NOT NULL,
  `chk_id` int(11) NOT NULL,
  `cpu_pct` decimal(19,2) NOT NULL,
  `hostname` varchar(255) NOT NULL,
  `ip` varchar(255) NOT NULL,
  `date_recorded` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

CREATE TABLE `data_diskhardware` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hostid` int(11) NOT NULL,
  `chk_id` int(11) NOT NULL,
  `mount_point` text NOT NULL,
  `hostname` varchar(255) NOT NULL,
  `ip` varchar(255) NOT NULL,
  `date_recorded` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;


 CREATE TABLE `data_osinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hostid` int(11) NOT NULL,
  `chk_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `uname` varchar(255) NOT NULL,
  `platform` varchar(255) NOT NULL,
  `architecture` varchar(255) NOT NULL,
  `release` varchar(255) NOT NULL,
  `version` varchar(255) NOT NULL,
  `hostname` varchar(255) NOT NULL,
  `ip` varchar(255) NOT NULL,
  `date_recorded` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

  osinfo['name'] = os.name
  osinfo['uname'] = sys.platform
  osinfo['platform'] = platform.machine()
  osinfo['architecture'] = platform.architecture()
  osinfo['release'] = platform.release()
  osinfo['version'] = platform.version()

{'name': 'posix', 
'uname': 'linux', 
'platform': 'x86_64', 
'architecture': ('64bit', 'ELF'), 
'release': '3.10.0-1160.24.1.el7.x86_64', 
'version': '#1 SMP Thu Apr 8 19:51:47 UTC 2021', 
'hostname': 'blackpanther', 
'ip': '192.168.1.31'}



select ch.*, cu.*, dh.*, du.*, mu.*, up.* from data_cpuhardware ch, data_cpuutilisation cu, data_diskhardware dh, data_diskutilisation du, data_memutilisation mu, data_uptime up where ch.hostid = cu.hostid and cu.hostid=1 order by cu.date_recorded desc limit 1;


