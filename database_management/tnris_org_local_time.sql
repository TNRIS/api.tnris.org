-- this sql needs to be run to create the rest endpoint properly formatted date/time for training courses

select title, start_date_time, end_date_time,
to_char(start_date_time at time zone 'America/Chicago', 'DD-MON-YYYY HH12:MI'),
to_char(end_date_time at time zone 'America/Chicago', 'DD-MON-YYYY HH12:MI' )
from tnris_training

-- returns two new columns. one column example: 'Monday October 21 08:00'. second column example ' - 12:00 PM'.
-- mash these two columsn together to get proper formatted date/time for tnris.org front end
-- final example format: 'Monday October 21 08:00 - 12:00 PM'
select title, start_date_time, end_date_time,
to_char(start_date_time at time zone 'America/Chicago', 'DayMonthDD HH24:MI'),
to_char(end_date_time at time zone 'America/Chicago', '- HH24:MI PM' )
from tnris_forum_training
