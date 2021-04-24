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


