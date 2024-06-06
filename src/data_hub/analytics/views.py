from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from lcd.models import Collection, TemplateType
from msd.models import MapCollection
from analytics.models import DownloadLog2024
import inspect
import analytics.models
from datetime import datetime
import time
import json
from django.db import connections

AVG_TIME_TO_COMPLETE_HRS = 3
AVG_HOURLY_SALARY = 26.66

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

@login_required(login_url='/admin/login/')
def get_monthly_stats(request):
    # set up start and end time
    default_end_date = datetime.now()
    default_start_date = default_end_date.replace(day=1)
    start_date = request.GET.get('start_date', default_start_date.strftime('%Y-%m-%d'))
    end_date = request.GET.get('end_date', default_end_date.strftime('%Y-%m-%d'))
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        if start_date >= end_date:
            raise Exception('start date must be before end date')
    except ValueError:
        print('dates must be in the form YYYY-M-D') 
        raise   
    except Exception:
        print('start date must be after end date')
        raise

    # initialize no_downloads with all possible collections (we remove any that were downloaded)
    no_downloads = {}
    collections = Collection.objects.filter(template_type_id__template='tnris-download').using('default')
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
              where x_edge_result_type <> 'Error!'
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
                when hist_product = 'cog' and hist_file like '%_idx.zip' then 
                       'historic imagery '||hist_type||'boundry shapefile'
                else 'historic imagery '||hist_type||hist_product
              end) as category, 
              count(*) from download_log_{0} 
            where x_edge_result_type <> 'Error'
									  and collection_id = ''
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
