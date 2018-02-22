-- drop index c__ip_index on proxies.tmp;
drop table if exists proxies.tmp;


CREATE TABLE proxies.tmp (
counter bigint unsigned PRIMARY KEY AUTO_INCREMENT NOT NULL,
c__ip varchar(16),
cs__username varchar(255),
c__agent text,
sc__authenticated varchar(1),
date date,
TIME TIME,
s__svcname varchar(100),
s__computername varchar(26),
cs__referred text,
r__host varchar(150),
r__ip varchar(16),
r__port smallint unsigned,
time__taken int,
sc__bytes int,
cs__bytes int,
cs__protocol varchar(32),
cs__transport varchar(6),
s__operation varchar(32),
cs__uri text,
cs__mime__type varchar(50),
s__object__source varchar(255),
sc__status smallint unsigned,
s__cache__info varchar(10),
RULE text,
filterinfo text,
cs__network varchar(255),
sc__network varchar(255),
error__info varchar(10),
action varchar(64),
gmt__time datetime,
authenticationserver varchar(64),
nis__scan__result varchar(64),
nis__signature varchar(64),
threatname varchar(64),
malwareinspectionaction varchar(64),
malwareinspectionresult varchar(64),
urlcategory varchar(64),
malwareinspectioncontentdeliverymethod varchar(64),
mi__uagarrayid varchar(64),
sc__uagversion varchar(64),
mi__uagmoduleid varchar(64),
sc__uagid varchar(64),
mi__uagseverity varchar(64),
mi__uagtype varchar(64),
sc__uageventname varchar(64),
mi__uagsessionid varchar(64),
mi__uagtrunkname varchar(64),
mi__uagservicename varchar(64),
sc__uagerrorcode varchar(64),
malwareinspectionduration varchar(64),
malwareinspectionthreatlevel varchar(64),
internal__service__info varchar(64),
nis__application__protocol varchar(64),
nat__address varchar(64),
urlcategorizationreason varchar(64),
sessiontype varchar(64),
urldesthost varchar(255),
s__port smallint unsigned,
softblockaction varchar(255));


CREATE INDEX c__ip_index ON proxies.tmp (c__ip);
CREATE INDEX username_index ON proxies.tmp (cs__username);
CREATE INDEX date_index on proxies.tmp (date);
CREATE INDEX time_index on proxies.tmp (time);
create index sc_bytes_index on proxies.tmp (sc_bytes);


-- CREATE INDEX c__ip_index ON tmp (c__ip);
