#!/bin/bash

domain=stagingapi.tnris.org/
paths_array=(
    "admin/login/?next=/admin/"
    "api/v1/schema/"

    "api/v1/areas"

    "api/v1/collections"

    "api/v1/collections_catalog"

    "api/v1/contact/survey"

    "api/v1/historical/collections"
    "api/v1/historical/counties"
    "api/v1/historical/mapserver"
    "api/v1/historical/records"

    "api/v1/map/collections"

    "api/v1/resources"

    "api/v1/tnris_org/carousel_image"
    "api/v1/tnris_org/comm_note"
    "api/v1/tnris_org/complete_forum_training"
    "api/v1/tnris_org/forum_training"
    "api/v1/tnris_org/gio_calendar"
    "api/v1/tnris_org/instructor_type"
    "api/v1/tnris_org/sgm_note"
    "api/v1/tnris_org/training"
)
# contact form submission POST?

echo running api endpoint ping tests...

for p in ${paths_array[*]}; do
    url=://$domain$p

    echo https$url
    res=$(curl -s -o /dev/null -w "%{http_code}" https$url);
    if [ $res -ne 200 ] ; then
        echo "FAIL! expected 200, received $res"
        return 1
    fi
done

echo finished successfully