delete from "dataMun_week";
delete from "dataMun_diagnosticcases" ;

-- deleting cols useless
delete from raw where col0 is null;
select week from raw;
-- sql datazone
insert into "dataMun_zone" (code)
select DISTINCT col0 from raw where col0 not in (select code from "dataMun_zone");

--- center
insert into "dataMun_center" (code,name,zone_id)
select DISTINCT col1, col2, (select dz.id from "dataMun_zone" dz where col0 = dz.code)
from raw where col1 not in (select code from "dataMun_center");

-- diagnostic
insert into "dataMun_diagnostic" (code,name)
select DISTINCT col3, col4
from raw where col3 not in (select code from "dataMun_diagnostic");

-- year
insert into "dataMun_year" (year)
select distinct r.year from raw r
where r."year" not in(select "year" from "dataMun_year");

-- week
insert into "dataMun_week" (week,year_id,creation)
select distinct r.week, (SELECT dy.id from dataMun_year dy where dy.year = r.year),current_date
from raw r where r.week not in (select week from "dataMun_week") and r."year" not in (select "year" from "dataMun_week");
SELECT *FROM  dataMun_week dmw ;
--
insert into "dataMun_sex"(name) values ('Male');
insert into "dataMun_sex"(name) values ('Female');

insert into "dataMun_age" (from_age,to_age) values(0,1);
insert into "dataMun_age" (from_age,to_age) values(1,5);
insert into "dataMun_age" (from_age,to_age) values(6,9);
insert into "dataMun_age" (from_age,to_age) values(10,14);
insert into "dataMun_age" (from_age,to_age) values(15,19);
insert into "dataMun_age" (from_age,to_age) values(20,54);
insert into "dataMun_age" (from_age,to_age) values(55,65);
insert into "dataMun_age" (from_age,to_age) values(65,214748367);

SELECT * from dataMun_age dma ;
-- diagnostic cases

select * from "dataMun_age" dma ;
-- cases <1 M
insert into "dataMun_diagnosticcases" (creation, cases, center_id, diagnostic_id, week_id, sex_id, age_id)
select current_date,
	col5,
	(select dc.id from "dataMun_center" dc where raw.col1 = dc.code ),
	(select dd.id from "dataMun_diagnostic" dd where raw.col3 = dd.code),
	(select dw.id from "dataMun_week" dw where raw.week = dw.week),
	(select ds.id from "dataMun_sex" ds where ds.name like 'M%'),
	(select da.id from "dataMun_age" da where da.from_age = 0)
from raw where col5 is not null and col5 not in (select cases from "dataMun_diagnosticcases" where sex_id=1 and age_id = (select da.id from "dataMun_age" da where da.from_age = 0))
;

-- cases <1 F
insert into "dataMun_diagnosticcases" (creation, cases, center_id, diagnostic_id, week_id, sex_id, age_id)
select current_date,
	col6,
	(select dc.id from "dataMun_center" dc where raw.col1 = dc.code ),
	(select dd.id from "dataMun_diagnostic" dd where raw.col3 = dd.code),
	(select dw.id from "dataMun_week" dw where raw.week = dw.week),
	(select ds.id from "dataMun_sex" ds where ds.name like 'F%'),
	(select da.id from "dataMun_age" da where da.from_age = 0)
from raw where col6 is not null and col6 not in (select cases from "dataMun_diagnosticcases" where sex_id=2 and age_id=(select da.id from "dataMun_age" da where da.from_age = 0))
;

-- cases 1 to 5 M
insert into "dataMun_diagnosticcases" (creation, cases, center_id, diagnostic_id, week_id, sex_id, age_id)
select current_date,
	col7,
	(select dc.id from "dataMun_center" dc where raw.col1 = dc.code ),
	(select dd.id from "dataMun_diagnostic" dd where raw.col3 = dd.code),
	(select dw.id from "dataMun_week" dw where raw.week = dw.week),
	(select ds.id from "dataMun_sex" ds where ds.name like 'M%'),
	(select da.id from "dataMun_age" da where da.from_age = 1)
from raw where col7 is not null and col7 not in (select cases from "dataMun_diagnosticcases" where sex_id=1 and age_id=(select da.id from "dataMun_age" da where da.from_age = 1))
;

select  * from "dataMun_age" dma where from_age = 1;
-- cases 1 to 5 F
insert into "dataMun_diagnosticcases" (creation, cases, center_id, diagnostic_id, week_id, sex_id, age_id)
select current_date,
	col8,
	(select dc.id from "dataMun_center" dc where raw.col1 = dc.code ),
	(select dd.id from "dataMun_diagnostic" dd where raw.col3 = dd.code),
	(select dw.id from "dataMun_week" dw where raw.week = dw.week),
	(select ds.id from "dataMun_sex" ds where ds.name like 'F%'),
	(select da.id from "dataMun_age" da where da.from_age = 1)
from raw where col8 is not null and col8 not in (select cases from "dataMun_diagnosticcases" where sex_id=2 and age_id=(select da.id from "dataMun_age" da where da.from_age = 1))
;

-- cases 6 to 9 M
insert into "dataMun_diagnosticcases" (creation, cases, center_id, diagnostic_id, week_id, sex_id, age_id)
select current_date,
	col9,
	(select dc.id from "dataMun_center" dc where raw.col1 = dc.code ),
	(select dd.id from "dataMun_diagnostic" dd where raw.col3 = dd.code),
	(select dw.id from "dataMun_week" dw where raw.week = dw.week),
	(select ds.id from "dataMun_sex" ds where ds.name like 'M%'),
	(select da.id from "dataMun_age" da where da.from_age = 6)
from raw where col9 is not null and col9 not in (select cases from "dataMun_diagnosticcases" where sex_id=1 and age_id = (select da.id from "dataMun_age" da where da.from_age = 6))
;

-- cases 6 to 9 F
insert into "dataMun_diagnosticcases" (creation, cases, center_id, diagnostic_id, week_id, sex_id, age_id)
select current_date,
	col10,
	(select dc.id from "dataMun_center" dc where raw.col1 = dc.code ),
	(select dd.id from "dataMun_diagnostic" dd where raw.col3 = dd.code),
	(select dw.id from "dataMun_week" dw where raw.week = dw.week),
	(select ds.id from "dataMun_sex" ds where ds.name like 'F%'),
	(select da.id from "dataMun_age" da where da.from_age = 6)
from raw where col10 is not null and col10 not in (select cases from "dataMun_diagnosticcases" where sex_id=2 and age_id=(select da.id from "dataMun_age" da where da.from_age = 6))
;
-- cases 10 to 14 M
insert into "dataMun_diagnosticcases" (creation, cases, center_id, diagnostic_id, week_id, sex_id, age_id)
select current_date,
	col11,
	(select dc.id from "dataMun_center" dc where raw.col1 = dc.code ),
	(select dd.id from "dataMun_diagnostic" dd where raw.col3 = dd.code),
	(select dw.id from "dataMun_week" dw where raw.week = dw.week),
	(select ds.id from "dataMun_sex" ds where ds.name like 'M%'),
	(select da.id from "dataMun_age" da where da.from_age = 10)
from raw where col11 is not null and col11 not in (select cases from "dataMun_diagnosticcases" where sex_id=1 and age_id=(select da.id from "dataMun_age" da where da.from_age = 10))
;
-- cases 10 to 14 F
insert into "dataMun_diagnosticcases" (creation, cases, center_id, diagnostic_id, week_id, sex_id, age_id)
select current_date,
	col12,
	(select dc.id from "dataMun_center" dc where raw.col1 = dc.code ),
	(select dd.id from "dataMun_diagnostic" dd where raw.col3 = dd.code),
	(select dw.id from "dataMun_week" dw where raw.week = dw.week),
	(select ds.id from "dataMun_sex" ds where ds.name like 'F%'),
	(select da.id from "dataMun_age" da where da.from_age = 10)
from raw where col12 is not null and col12 not in (select cases from "dataMun_diagnosticcases" where sex_id=2 and age_id=(select da.id from "dataMun_age" da where da.from_age = 10))
;

-- 15 to 19 m
insert into "dataMun_diagnosticcases" (creation, cases, center_id, diagnostic_id, week_id, sex_id, age_id)
select current_date,
	col13,
	(select dc.id from "dataMun_center" dc where raw.col1 = dc.code ),
	(select dd.id from "dataMun_diagnostic" dd where raw.col3 = dd.code),
	(select dw.id from "dataMun_week" dw where raw.week = dw.week),
	(select ds.id from "dataMun_sex" ds where ds.name like 'M%'),
	(select da.id from "dataMun_age" da where da.from_age = 15)
from raw where col13 is not null and col13 not in (select cases from "dataMun_diagnosticcases" where sex_id=1 and age_id=(select da.id from "dataMun_age" da where da.from_age = 15))
;

-- 15 to 19 f
insert into "dataMun_diagnosticcases" (creation, cases, center_id, diagnostic_id, week_id, sex_id, age_id)
select current_date,
	col14,
	(select dc.id from "dataMun_center" dc where raw.col1 = dc.code ),
	(select dd.id from "dataMun_diagnostic" dd where raw.col3 = dd.code),
	(select dw.id from "dataMun_week" dw where raw.week = dw.week),
	(select ds.id from "dataMun_sex" ds where ds.name like 'F%'),
	(select da.id from "dataMun_age" da where da.from_age = 15)
from raw where col14 is not null and col14 not in (select cases from "dataMun_diagnosticcases" where sex_id=2 and age_id=(select da.id from "dataMun_age" da where da.from_age = 15))
;

-- 20 to 54 m
insert into "dataMun_diagnosticcases" (creation, cases, center_id, diagnostic_id, week_id, sex_id, age_id)
select current_date,
	col15,
	(select dc.id from "dataMun_center" dc where raw.col1 = dc.code ),
	(select dd.id from "dataMun_diagnostic" dd where raw.col3 = dd.code),
	(select dw.id from "dataMun_week" dw where raw.week = dw.week),
	(select ds.id from "dataMun_sex" ds where ds.name like 'M%'),
	(select da.id from "dataMun_age" da where da.from_age = 20)
from raw where col15 is not null and col15 not in (select cases from "dataMun_diagnosticcases" where sex_id=1 and age_id=(select da.id from "dataMun_age" da where da.from_age = 20))
;

-- 20 to 54 f
insert into "dataMun_diagnosticcases" (creation, cases, center_id, diagnostic_id, week_id, sex_id, age_id)
select current_date,
	col16,
	(select dc.id from "dataMun_center" dc where raw.col1 = dc.code ),
	(select dd.id from "dataMun_diagnostic" dd where raw.col3 = dd.code),
	(select dw.id from "dataMun_week" dw where raw.week = dw.week),
	(select ds.id from "dataMun_sex" ds where ds.name like 'F%'),
	(select da.id from "dataMun_age" da where da.from_age = 20)
from raw where col16 is not null and col16 not in (select cases from "dataMun_diagnosticcases" where sex_id=2 and age_id=(select da.id from "dataMun_age" da where da.from_age = 20))
;

-- 55 to 65 m
insert into "dataMun_diagnosticcases" (creation, cases, center_id, diagnostic_id, week_id, sex_id, age_id)
select current_date,
	col17,
	(select dc.id from "dataMun_center" dc where raw.col1 = dc.code ),
	(select dd.id from "dataMun_diagnostic" dd where raw.col3 = dd.code),
	(select dw.id from "dataMun_week" dw where raw.week = dw.week),
	(select ds.id from "dataMun_sex" ds where ds.name like 'M%'),
	(select da.id from "dataMun_age" da where da.from_age = 55)
from raw where col17 is not null and col17 not in (select cases from "dataMun_diagnosticcases" where sex_id=1 and age_id=(select da.id from "dataMun_age" da where da.from_age = 55))
;

-- 55 to 65 f
insert into "dataMun_diagnosticcases" (creation, cases, center_id, diagnostic_id, week_id, sex_id, age_id)
select current_date,
	col18,
	(select dc.id from "dataMun_center" dc where raw.col1 = dc.code ),
	(select dd.id from "dataMun_diagnostic" dd where raw.col3 = dd.code),
	(select dw.id from "dataMun_week" dw where raw.week = dw.week),
	(select ds.id from "dataMun_sex" ds where ds.name like 'F%'),
	(select da.id from "dataMun_age" da where da.from_age = 55)
from raw where col18 is not null and col18 not in (select cases from "dataMun_diagnosticcases" where sex_id=2 and age_id=(select da.id from "dataMun_age" da where da.from_age = 55))
;
-- more than 65 m
insert into "dataMun_diagnosticcases" (creation, cases, center_id, diagnostic_id, week_id, sex_id, age_id)
select current_date,
	col19,
	(select dc.id from "dataMun_center" dc where raw.col1 = dc.code ),
	(select dd.id from "dataMun_diagnostic" dd where raw.col3 = dd.code),
	(select dw.id from "dataMun_week" dw where raw.week = dw.week),
	(select ds.id from "dataMun_sex" ds where ds.name like 'M%'),
	(select da.id from "dataMun_age" da where da.from_age = 65)
from raw where col19 is not null and col19 not in (select cases from "dataMun_diagnosticcases" where sex_id=1 and age_id=(select da.id from "dataMun_age" da where da.from_age = 65))
;

-- more than 65 f
insert into "dataMun_diagnosticcases" (creation, cases, center_id, diagnostic_id, week_id, sex_id, age_id)
select current_date,
	col20,
	(select dc.id from "dataMun_center" dc where raw.col1 = dc.code ),
	(select dd.id from "dataMun_diagnostic" dd where raw.col3 = dd.code),
	(select dw.id from "dataMun_week" dw where raw.week = dw.week),
	(select ds.id from "dataMun_sex" ds where ds.name like 'F%'),
	(select da.id from "dataMun_age" da where da.from_age = 65)
from raw where col20 is not null and col20 not in (select cases from "dataMun_diagnosticcases" where sex_id=2 and age_id=(select da.id from "dataMun_age" da where da.from_age = 65))
;
SELECT * from dataMun_diagnosticcases dmd;

