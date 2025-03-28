from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, QueryDict
from django.contrib.auth.decorators import login_required
from lcd.models import Collection, TemplateType
from msd.models import MapCollection
import inspect
import os
from datetime import datetime
import time
import json
from django.db import connections
import requests

AVG_TIME_TO_COMPLETE_HRS = 3
AVG_HOURLY_SALARY = 26.66

all_services = None

# convert dollar totals from e.g. 1,000,000 to 1M 
def format_money(num):
    if num > 1000000000:
        if not num % 1000000000:
            return f'${num // 1000000000}B'
        return f'${round(num / 1000000000, 1)}B'
    elif num > 1000000:
        if not num % 1000000:
            return f'${num // 1000000}M'
        return f'${round(num / 1000000, 1)}M'
    elif num > 1000:
        if not num % 1000:
            return f'${num // 1000}K'
        return f'${num // 1000}K'
    return f'${num}'

def get_default_start_and_end_dates():
    # get the date/time for the report (defaults to the start of the month until today or last month if today is the 1st)
    default_end_date = datetime.now()
    default_start_date = default_end_date.replace(day=1)
    # if it's the first of the month, make the default start the first of last month
    if (default_end_date.day == 1):
        last_month = default_end_date.month - 1
        print(last_month)
        if last_month == 0:
            last_month = 12
        default_start_date = default_end_date.replace(month=last_month)   
    return [default_start_date, default_end_date] 

def get_arcgis_token():
    # retrieve token used to make requests
    username = os.environ.get('ARCGIS_USERNAME')
    password = os.environ.get('ARCGIS_PASSWORD')
    data = {'username': username, 'password': password, 'client': 'requestip', 'expiration': 90, 'f': 'json'}
    response = requests.post("https://feature.geographic.texas.gov/arcgis/admin/generateToken", data=data)
    token = response.json()['token']
    print(token)
    return token

@login_required(login_url='/admin/login/')
def get_all_service_and_subservices(request):
    # initialize the list of services and subservices and their shown status
    global all_services
    if all_services is not None:
        return JsonResponse(all_services, safe=False)
    
    token = get_arcgis_token()    
    # response = requests.get('https://feature.geographic.texas.gov/arcgis/admin/usagereports/analytics_dashboard?f=json&token=' + token)
    # currentServices = response.json()["queries"][0]["resourceURIs"]
    # print("currentServices " + str(currentServices))

    all_services = [
        {  "serviceName": "services/", "isShown": True },
        {  "serviceName": "services/Address_Points", "isShown": False },
        {  "serviceName": "services/Basemap", "isShown": False },
        {  "serviceName": "services/Bathymetry", "isShown": False },
        {  "serviceName": "services/FDST", "isShown": False },
        {  "serviceName": "services/Geologic_Database", "isShown": False },
        {  "serviceName": "services/Hydrography", "isShown": False },
        {  "serviceName": "services/Hypsography", "isShown": False },
        {  "serviceName": "services/Parcels", "isShown": False }
    ]
    for s in all_services:
        print("serviceName")
        print(s["serviceName"])
        # if s["serviceName"] in currentServices:
        #     s["isShown"] = True
        actualServiceName = s["serviceName"].split("/")[1]
        if not actualServiceName: # i.e. just "services/"
            continue
        # otherwise, get all the subservices there are
        response = requests.get('https://feature.geographic.texas.gov/arcgis/admin/services/' + actualServiceName + '?f=json&token=' + token)
        # print(response.text)
        s["subservices"] = []
        for subservice in response.json()["services"]:
            print("subserviceName")
            print(subservice["serviceName"])
            subserviceFullName = s["serviceName"] + "/" + subservice["serviceName"] + ".MapServer"
            # isShown = subserviceFullName in currentServices
            s["subservices"].append({"serviceName": subserviceFullName, "isShown": False})
            
    return JsonResponse(all_services, safe=False)

@login_required(login_url='/admin/login/')
def update_services_in_arcgis_report(request):
    print("in update services")
    token = get_arcgis_token()
    print("reportName from request" + str(request.POST.get("reportName")))
    reportName = request.POST.get("reportName")
    resourceURIs = request.POST.get("resourceURIs")
    print("request method is ")
    print(request.method)
    print(reportName)
    print(resourceURIs)

    # default_dates = get_default_start_and_end_dates()
    # start_date = request.POST.get('start_date', default=round(default_dates[0].timestamp() / 100) * 100000)
    # end_date = request.POST.get('end_date', default=round(default_dates[1].timestamp() / 100) * 100000)
    # # for some reason, the default argument isn't working, so using the code below
    # if (not start_date): 
    #     start_date = str(round(default_dates[0].timestamp() / 100) * 100000)
    # if (not end_date): 
    #     end_date = str(round(default_dates[1].timestamp() / 100) * 100000)
    # print('from', start_date)
    # print('to', end_date)


    # queries ='"queries":[]'
    # if len(resourceURIs) > 0:
    #     queries = '"queries":[{"resourceURIs":' + str(resourceURIs) + ',"metrics":["RequestCount"]}]'
    # print("queries " + queries)
    # data = {'usagereport': '{"reportname":"' + reportName + '","since":"CUSTOM",' + str(queries) + ',"metadata":{"temp":false,"title":"Total requests for the last 7 days","managerReport":true,"styles":{"services/":{"color":"#D900D9"}}},"from":' + str(start_date) + ',"to":' + str(end_date) + '}', 'f': 'json', 'token': token}
    # print("edit data " + str(data))

    # response = requests.get('https://feature.geographic.texas.gov/arcgis/admin/usagereports/' + reportName + '?f=json&token=' + token)
    # print("first request " + response.status_code)
    # # check if 404 error    
    # if (response.status_code == 404):
    #     response = requests.post('https://feature.geographic.texas.gov/arcgis/admin/usagereports/add', data=data)
    # else:
    #     response = requests.post('https://feature.geographic.texas.gov/arcgis/admin/usagereports/analytics_dashboard/edit', data=data)

    # print(response.txt)
    return HttpResponse("OK")

    # When update successfully returns, call get stats from arcgis.  
    # tear out all the code to edit the report

@login_required(login_url='/admin/login/')
def get_stats_from_arcgis(request):
    global all_services

    token = get_arcgis_token()

    print(str(all_services))

    # toggle the service listed in the request and 
    # add any shown service to the list of resourceURIs
    serviceToToggle = request.GET.get("serviceToToggle")
    print("service to toggle")
    print(serviceToToggle)
    resourceURIs = []
    for service in all_services:
        if service["serviceName"] == serviceToToggle:
            service["isShown"] = not service["isShown"]
        if service["isShown"]:
            resourceURIs.append(service["serviceName"])
        if "subservices" in service:
            for subservice in service['subservices']:
                if subservice["serviceName"] == serviceToToggle:
                    subservice["isShown"] = not subservice["isShown"]
                if subservice["isShown"]:
                    resourceURIs.append(subservice["serviceName"])

    print("resourceURIs " + str(resourceURIs))         
    response = requests.get('https://feature.geographic.texas.gov/arcgis/admin/usagereports/analytics_dashboard?f=json&token=' + token)
    print("first request " + response.text)

    default_dates = get_default_start_and_end_dates()
    start_date = request.GET.get('start_date', default=round(default_dates[0].timestamp() / 100) * 100000)
    end_date = request.GET.get('end_date', default=round(default_dates[1].timestamp() / 100) * 100000)
    # for some reason, the default argument isn't working, so using the code below
    if (not start_date): 
        start_date = str(round(default_dates[0].timestamp() / 100) * 100000)
    if (not end_date): 
        end_date = str(round(default_dates[1].timestamp() / 100) * 100000)
    print('from', start_date)
    print('to', end_date)
    # edit the report called analytics_dashboard to reflect the select dates and services the user is interested in
    queries ='"queries":[]'
    if len(resourceURIs) > 0:
        queries = '"queries":[{"resourceURIs":' + str(resourceURIs) + ',"metrics":["RequestCount"]}]'
    print("queries " + queries)
    data = {'usagereport': '{"reportname":"analytics_dashboard","since":"CUSTOM",' + str(queries) + ',"metadata":{"temp":false,"title":"Total requests for the last 7 days","managerReport":true,"styles":{"services/":{"color":"#D900D9"}}},"from":' + str(start_date) + ',"to":' + str(end_date) + '}', 'f': 'json', 'token': token}
    print("edit data " + str(data))
    response = requests.post('https://feature.geographic.texas.gov/arcgis/admin/usagereports/analytics_dashboard/edit', data=data)
    # print(response.request.body)
    print(response.text)
    # get the report data
    response = requests.get('https://feature.geographic.texas.gov/arcgis/admin/usagereports/analytics_dashboard/data?filter=%7B%22services%22%3A%22*%22%2C%22machines%22%3A%22*%22%7D&f=json&token=' + token)
    print("final response " + response.text)
    return HttpResponse(response.text)


@login_required(login_url='/admin/login/')
def get_monthly_stats(request):
    # set up start and end time
    default_dates = get_default_start_and_end_dates()
    start_date = request.GET.get('start_date', default_dates[0].strftime('%Y-%m-%d'))
    end_date = request.GET.get('end_date', default_dates[1].strftime('%Y-%m-%d'))
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        if start_date >= end_date:
            # raise Exception('start date must be before end date')
            return render(request, 'stats.html', {'error', 'Start date must be before end date'})
    except ValueError:
        print('dates must be in the form YYYY-M-D') 
        return render(request, 'stats.html', {'error', 'Dates must be in the form YYYY-M-D'})
        # raise   
    except Exception:
        print('You must provide both a start and end date')
        return render(request, 'stats.html', {'error', 'You must provide both a start and end date'})
        # raise

    # initialize no_downloads with all possible collections (we remove any that were downloaded)
    no_downloads = {}
    collections = Collection.objects.filter(template_type_id__template='tnris-download').filter(public__exact=True).using('default')
    for coll in collections:
        no_downloads[str(coll.collection_id)] = "%s %s" % (coll.acquisition_date[:4], coll.name)

    # query clauses used to compose the actual SQL queries
    def print_raw_query_set(qs):
        for row in qs:
            print(row)

    total_queries = {
        'total_downloads':
        """
        select {0} from download_log_{1}
        """,
        'total_success_data':
        """
        select {0} from download_log_{1}
                         where x_edge_result_type <> 'Error'
                         and ((collection_id <> '' and area_type_id <> 'map') or collection_id = '')
        """,
        'total_success_map':
        """
        select {0} from download_log_{1} 
                        where x_edge_result_type <> 'Error'
                        and collection_id <> '' 
                        and area_type_id = 'map'
        """,
        'total_errors':
        """

        select {0} from download_log_{1} 
                        where x_edge_result_type = 'Error'
        """
    }
    queries = {
        'all_collections':
            {'select_statement':
              """
              select collection_id from download_log_{0}
              where collection_id <> ''
              """,
             'grouping_clause': ''
            },
            # substring(cs_uri_stem from '([^\/]*$)') as cs_uri_stem, 
        'count_by_key': 
            {'select_statement': 
              """
              select collection_id, count(collection_id) from download_log_{0}
              where collection_id <> '' and x_edge_result_type <> 'Error!'
              """,
            'grouping_clause': 
            """
                group by collection_id{0}
                order by count desc
            """},
        'count_by_collection': 
            {'select_statement': 
            """
            select 
              (case 
                when collection_id = '' then hist_collective||' '||hist_mission||' ('||hist_band||')'
              else collection_shortname
              end) as category, 
              count(*) from download_log_{0} 
            where x_edge_result_type <> 'Error'
            """, 
            'grouping_clause': 
            """
              group by category{0}
              order by count desc
            """},
        'count_by_map': 
            {'select_statement': 
             """
            select collection_shortname, count(collection_shortname) from download_log_{0} 
                    where x_edge_result_type <> 'Error'
									  and collection_id <> ''
									  and area_type_id = 'map'
            """, 
            'grouping_clause': 
            """
            group by collection_shortname{0}
            order by count desc
            """},
        'count_by_historic': 
            {'select_statement': 
            """
            select 
              hist_collective||' '||hist_mission||' ('||hist_band||')' as historic_imagery_shortname, 
              count(*) from download_log_{0} 
            where x_edge_result_type <> 'Error'
									  and collection_id = ''
            """,
            'grouping_clause': 
            """
            group by historic_imagery_shortname{0}
            order by count desc
            """},
        'count_by_resource_type': 
            {'select_statement': 
            """
            select 
              (case
			  	when collection_id <> '' then
				  file_type
			    else 
				  (case 
	                when hist_product = 'cog' and hist_file like '%_idx.zip' then 
	                       'historic imagery '||hist_type||'boundry shapefile'
	                else 'historic imagery '||hist_type||' '||hist_product
	              end)
			  end) as category, 
              count(*) from download_log_{0} 
            where x_edge_result_type <> 'Error'
            """,
            'grouping_clause': 
            """
									  group by category{0}
									  order by count desc
            """},
        'count_by_error': 
            {'select_statement': 
            """
            select 
              x_edge_detailed_result_type,
              (case 
                when collection_id = '' then hist_collective||' '||hist_mission||' ('||hist_band||')'
              else collection_shortname
              end) as category, 
              count(*) from download_log_{0} 
            where x_edge_result_type = 'Error'
            """,
            'grouping_clause': 
            """
									  group by x_edge_detailed_result_type, category{0}
									  order by count desc
            """}
        
    }

    # compose the queries
    start_year = start_date.year
    end_year = end_date.year
    start_time = time.time()
    results = {}
    start_date_clause = "date >= '" + start_date.strftime('%Y-%m-%d') + "'::DATE"
    end_date_clause = "date <= '" + end_date.strftime('%Y-%m-%d') + "'::DATE"
    total_success = 0
    # for queries like total_downloads
    for q in total_queries:
        beginning_of_date_clause = 'where ' if q == 'total_downloads' else 'and '
        select_statement = total_queries.get(q)
        # if start and end in the same year, we won't need to UNION anything 
        if start_year == end_year:
            query = select_statement.format('count(*)', str(start_year))
            query += beginning_of_date_clause + start_date_clause + ' and ' + end_date_clause
        # otherwise we need to UNION the logs from different years
        else:
            query = select_statement.format('id', str(start_year))
            query = '(' + query + ' ' + beginning_of_date_clause + start_date_clause
            year = start_year + 1            
            while year <= end_year:
                query += ') union ('
                query += select_statement.format('id', str(year))
                year += 1
            query += ' ' + beginning_of_date_clause + end_date_clause + ')'
            query = 'select count(*) from (' + query + ') as all_years'
        print(query)
        with connections['analytics'].cursor() as cursor:
            cursor.execute(query) 
            results[q] = cursor.fetchall()  
            if q == 'total_success_data' or q == 'total_success_map':
                total_success += results[q][0][0]
            results[q] = f'{results[q][0][0]:,}'
    hours_saved = total_success * AVG_TIME_TO_COMPLETE_HRS
    dollars_saved = hours_saved * AVG_HOURLY_SALARY
    results['total_success'] = f'{total_success:,}'
    results['hours_saved'] = f'{hours_saved:,}'
    results['dollars_saved'] = format_money(dollars_saved)

    # compose queries for top 10 lists
    for q in queries:
        select_statement = queries.get(q).get('select_statement')
        grouping_clause = queries.get(q).get('grouping_clause')
        final_clause = grouping_clause.format(', count') + ' limit 10'
        grouping_clause = grouping_clause.format('')

        query = select_statement.format(str(start_year))
        if start_year == end_year:
            query += 'and ' + start_date_clause + ' and ' + end_date_clause + grouping_clause + ' limit 10'
        else:
            query = '(' + query + ' ' + 'and ' + start_date_clause
            year = start_year + 1
        
            while year <= end_year:
                query += grouping_clause + ') union ('
                query += select_statement.format(str(year))
                year += 1
            query += ' and ' + end_date_clause + grouping_clause + ')'
            query = 'select * from (' + query + ') as all_years' + final_clause

        print(query)
        with connections['analytics'].cursor() as cursor:
            cursor.execute(query) 
            results[q] = cursor.fetchall()  


    print(results['count_by_key'])
    for i, result in enumerate(results['count_by_key']):
        print(result[0])
        coll = None
        isMap = False
        try:
            coll = Collection.objects.get(pk=result[0])
        except Collection.DoesNotExist:
            coll = MapCollection.objects.get(pk=result[0])
            isMap = True
        if isMap:
            print(coll.name + ' ' + str(coll.publish_date))
            results['count_by_key'][i] = (coll.name + ' ' + str(coll.publish_date), result[1])
        else:
            print(coll.name + ' ' + coll.acquisition_date)
            results['count_by_key'][i] = (coll.name + ' ' + coll.acquisition_date, result[1])
    print(results['count_by_key'])

    print(results['all_collections'][0])

    print("iterating through queries takes ", time.time() - start_time)
    return render(request, 'stats.html', results) 
