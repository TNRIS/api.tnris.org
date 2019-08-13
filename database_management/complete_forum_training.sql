-- Create complete tnris forum training view
-- includes related instructor types

DROP VIEW IF EXISTS "complete_forum_training";

CREATE VIEW "complete_forum_training" as
SELECT tnris_forum_training.training_id,
  tnris_forum_training.training_day,
  tnris_forum_training.title,
  tnris_forum_training.start_date_time,
  tnris_forum_training.end_date_time,
  tnris_forum_training.cost,
  tnris_forum_training.registration_open,
  tnris_forum_training.public,
  tnris_forum_training.location,
  tnris_forum_training.room,
  tnris_forum_training.max_students,
  tnris_forum_training.description,
  tnris_forum_training.teaser,
  array_to_string(ARRAY(SELECT json_build_object('instructor_name', tnris_instructor_type.name,
                                 'instructor_company', tnris_instructor_type.company,
                                 'instructor_bio', tnris_instructor_type.bio,
                                 'instructor_headshot', tnris_instructor_type.headshot)
        FROM tnris_instructor_type
        LEFT JOIN tnris_instructor_relate ON tnris_instructor_relate.instructor_relate_id=tnris_instructor_type.instructor_type_id
        WHERE tnris_instructor_relate.training_relate_id=tnris_forum_training.training_id), ',') as instructor_info

FROM tnris_forum_training
