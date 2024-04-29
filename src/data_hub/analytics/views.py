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
            results[q] = f'{results[q][0][0]:,}'

    # compose queries for top 10 lists
    for q in queries:
        select_statement = queries.get(q).get('select_statement')
        grouping_clause = queries.get(q).get('grouping_clause')
        final_clause = grouping_clause.format(', count') + ' limit 10'
        grouping_clause = grouping_clause.format('')
        # if q == 'count_by_key':
        #     final_clause = grouping_clause.format(', collection_id, count') + ' limit 10'
        # if q == 'count_by_key':
        #     grouping_clause = grouping_clause.format(', collection_id')
        # else:
        #     grouping_clause = grouping_clause.format('')

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
    # downloads_list = [coll[0] for coll in results['all_collections']]
    # results['total_downloadable'] = len(no_downloads.keys())
    # print(downloads_list[0])
    # for id in downloads_list:
    #     if id in no_downloads.keys():
    #         no_downloads.pop(str(id))
    # results['no_downloads'] = no_downloads
    # results['no_downloads_num'] = len(no_downloads)
    
    # print(results['count_by_key'][0])
    print("iterating through queries takes ", time.time() - start_time)
    return render(request, 'stats.html', results) 

# Create your views here.
# @login_required(login_url='/admin/login/')
# def hello_world(request):
#     return render(request, 'hello.html', {'reply': 'Hello, World'}) #HttpResponse('Hello, World')

# @login_required(login_url='/admin/login/')
# def get_monthly_stats_old(request):
#     no_downloads = {}
#     collections = Collection.objects.filter(template_type_id__template='tnris-download').using('default')
#     for coll in collections:
#         no_downloads[str(coll.collection_id)] = "%s %s" % (coll.acquisition_date[:4], coll.name)

#         # template_type = TemplateType.objects.get(coll.template_type_id).using('default')
#         # if template_type == 'tnris-download':
#     # print(list(no_downloads.keys()))
#     # print(collections['next'])

#     # start_time = time.time()
#     # logs = DownloadLog2024.objects.filter(date__gte=datetime.date(2024, 2, 1))
#     # print("query completed in %s" % (time.time() - start_time))
#     # print(logs.query)
#     # start_time = time.time()
#     # print(DownloadLog2024.objects.filter(date__gte=datetime.date(2024, 2, 1)).count())
#     # print("total downloads completed in %s" % (time.time() - start_time))
#     def print_raw_query_set(qs):
#         for row in qs:
#             print(row)

#     # start_time = time.time()
#     # print(len(list(DownloadLog2024.objects.raw("select id from download_log_2024 where date >= '2024-02-01'::date"))))
#     # print(DownloadLog2024.objects.raw("""
#     #     select cs_uri_stem, count(cs_uri_stem) from download_log_2024 
#     #                 where date >= '2024-02-01'::date
# 		# 							  and date <= '2024-02-29'::date
#     #                 and x_edge_result_type <> 'Error!'
# 		# 							  group by cs_uri_stem
# 		# 							  order by count desc
# 		# 							  limit 10
#     #     """))
#     # print(DownloadLog2024.objects.raw("""
#         # select collection_shortname, count(collection_shortname) from download_log_2024 
#         #             where date >= '2024-02-01'::date
# 				# 					  and date <= '2024-02-29'::date
#         #             and x_edge_result_type <> 'Error!'
# 				# 					  and collection_id <> ''
# 				# 					  and area_type_id <> 'map'
# 				# 					  group by collection_shortname
# 				# 					  order by count desc
# 				# 					  limit 10
#     #     """))
#     # print(DownloadLog2024.objects.raw("""
#     #     select collection_shortname, count(collection_shortname) from download_log_2024 
#     #                 where date >= '2024-02-01'::date
# 		# 							  and date <= '2024-02-29'::date
#     #                 and x_edge_result_type <> 'Error!'
# 		# 							  and collection_id <> ''
# 		# 							  and area_type_id = 'map'
# 		# 							  group by collection_shortname
# 		# 							  order by count desc
# 		# 							  limit 10
#     #     """))
#     # print(DownloadLog2024.objects.raw("""
#     #     select file_type, count(file_type) from download_log_2024 
#     #                 where date >= '2024-02-01'::date
# 		# 							  and date <= '2024-02-29'::date
#     #                 and x_edge_result_type <> 'Error!'
# 		# 							  and collection_id <> ''
# 		# 							  group by file_type
# 		# 							  order by count desc
# 		# 							  limit 10
#     #     """))
#     # print(DownloadLog2024.objects.raw("""
#     #     select file_type, count(file_type) from download_log_2024 
#     #                 where date >= '2024-02-01'::date
# 		# 							  and date <= '2024-02-29'::date
#     #                 and x_edge_result_type <> 'Error!'
# 		# 							  and collection_id <> ''
# 		# 							  group by file_type
# 		# 							  order by count desc
# 		# 							  limit 10
#     #     """))    
#     # print("total downloads completed in %s" % (time.time() - start_time))

#     total_queries = {
#         'total_downloads':
#         """
#         select {0} from download_log_{1}
#         """,
#         'total_success_data':
#         """
#         select {0} from download_log_{1}
#                          where x_edge_result_type <> 'Error'
#                          and ((collection_id <> '' and area_type_id <> 'map') or collection_id = '')
#         """,
#         'total_success_map':
#         """
#         select {0} from download_log_{1} 
#                         where x_edge_result_type <> 'Error'
#                         and collection_id <> '' 
#                         and area_type_id <> 'map'
#         """
#     }
#     queries = {
#         # 'total_downloads':
#         #     ["""
#         #     select count(*) from download_log_{0}
#         #     """],
#         'count_by_key': 
#             {'select_statement': 
#               """
#               select cs_uri_stem, count(cs_uri_stem) from download_log_{0}
#               where x_edge_result_type <> 'Error!'
#               """,
#             'grouping_clause': 
#             """
#                 group by cs_uri_stem{0}
#                 order by count desc
#             """},
#         'count_by_collection': 
#             {'select_statement': 
#             """
#             select 
#               (case 
#                 when collection_id = '' then hist_collective||' '||hist_mission||' ('||hist_band||')'
#               else collection_shortname
#               end) as category, 
#               count(*) from download_log_{0} 
#             where x_edge_result_type <> 'Error'
#             """, 
#             'grouping_clause': 
#             """
#               group by category{0}
#               order by count desc
#             """},
#         'count_by_map': 
#             {'select_statement': 
#              """
#             select collection_shortname, count(collection_shortname) from download_log_{0} 
#                     where x_edge_result_type <> 'Error'
# 									  and collection_id <> ''
# 									  and area_type_id = 'map'
#             """, 
#             'grouping_clause': 
#             """
#             group by collection_shortname{0}
#             order by count desc
#             """},
#         'count_by_historic': 
#             {'select_statement': 
#             """
#             select 
#               hist_collective||' '||hist_mission||' ('||hist_band||')' as historic_imagery_shortname, 
#               count(*) from download_log_{0} 
#             where x_edge_result_type <> 'Error'
# 									  and collection_id = ''
#             """,
#             'grouping_clause': 
#             """
#             group by historic_imagery_shortname{0}
#             order by count desc
#             """},
#         'count_by_resource_type': 
#             {'select_statement': 
#             """
#             select 
#               (case 
#                 when hist_product = 'cog' and hist_file like '%_idx.zip' then 
#                        'historic imagery '||hist_type||'boundry shapefile'
#                 else 'historic imagery '||hist_type||hist_product
#               end) as category, 
#               count(*) from download_log_{0} 
#             where x_edge_result_type <> 'Error'
# 									  and collection_id = ''
#             """,
#             'grouping_clause': 
#             """
# 									  group by category{0}
# 									  order by count desc
#             """},
#         'count_by_error': 
#             {'select_statement': 
#             """
#             select 
#               x_edge_detailed_result_type,
#               (case 
#                 when collection_id = '' then hist_collective||' '||hist_mission||' ('||hist_band||')'
#               else collection_shortname
#               end) as category, 
#               count(*) from download_log_{0} 
#             where x_edge_result_type = 'Error'
#             """,
#             'grouping_clause': 
#             """
# 									  group by x_edge_detailed_result_type, category{0}
# 									  order by count desc
#             """}
        
#     }

#     start_date = datetime.strptime('2022-01-01', '%Y-%m-%d')
#     end_date = datetime.strptime('2024-03-29', '%Y-%m-%d')
#     start_year = start_date.year
#     end_year = end_date.year
#     start_time = time.time()
#     results = {}
#     start_date_clause = "date >= '" + start_date.strftime('%Y-%m-%d') + "'::DATE"
#     end_date_clause = "date >= '" + end_date.strftime('%Y-%m-%d') + "'::DATE"
#     for q in total_queries:
#         beginning_of_date_clause = 'where ' if q == 'total_downloads' else 'and '
#         select_statement = total_queries.get(q)
#         if start_year == end_year:
#             query = select_statement.format('count(*)', str(start_year))
#             query += beginning_of_date_clause + start_date_clause + ' and ' + end_date_clause
#         else:
#             query = select_statement.format('id', str(start_year))
#             query = '(' + query + ' ' + beginning_of_date_clause + start_date_clause
#             year = start_year + 1            
#             while year <= end_year:
#                 query += ') union ('
#                 query += select_statement.format('id', str(year))
#                 year += 1
#             query += ' ' + beginning_of_date_clause + end_date_clause + ')'
#             query = 'select count(*) from (' + query + ') as all_years'
#         print(query)
#         with connections['analytics'].cursor() as cursor:
#             cursor.execute(query) 
#             results[q] = cursor.fetchall()  
#     for q in queries:
#         select_statement = queries.get(q).get('select_statement')
#         grouping_clause = queries.get(q).get('grouping_clause')
#         final_clause = grouping_clause.format(', count') + ' limit 10'
#         grouping_clause = grouping_clause.format('')
#         query = select_statement.format(str(start_year))
#         if start_year == end_year:
#             query += 'and ' + start_date_clause + ' and ' + end_date_clause + grouping_clause + ' limit 10'
#         else:
#             query = '(' + query + ' ' + 'and ' + start_date_clause
#             year = start_year + 1
        
#             while year <= end_year:
#                 query += grouping_clause + ') union ('
#                 query += select_statement.format(str(year))
#                 year += 1
#             query += ' and ' + end_date_clause + grouping_clause + ')'
#             query = 'select * from (' + query + ') as all_years' + final_clause

#         print(query)
#         with connections['analytics'].cursor() as cursor:
#             cursor.execute(query) 
#             results[q] = cursor.fetchall()  
#     print(results)
#     print("iterating through queries takes ", time.time() - start_time)
            
#     # start_time = time.time()
#     # with connections['analytics'].cursor() as cursor:
#     #     cursor.execute("""
#     #         select count(*) from download_log_2024 
#     #                     where date >= '2024-02-01'::date
#     #                     and date <= '2024-02-29'::date
#     #         """) 
#     #     total_downloads = cursor.fetchone()    
#     #     print("total ", total_downloads)   
#     #     cursor.execute("""
#     #         select count(*) from download_log_2024 
#     #                     where date >= '2024-02-01'::date
#     #                     and date <= '2024-02-29'::date
#     #                     and x_edge_result_type <> 'Error'
#     #                     and ((collection_id <> '' and area_type_id <> 'map') or collection_id = '')
#     #         """) 
#     #     total_success_data = cursor.fetchone()    
#     #     print("total ", total_success_data)   
#     #     cursor.execute("""collection
#     #         select count(*) from download_log_2024 
#     #                     where date >= '2024-02-01'::date
#     #                     and date <= '2024-02-29'::date
#     #                     and x_edge_result_type <> 'Error'
#     #                     and collection_id <> '' 
#     #                     and area_type_id <> 'map'
#     #         """) 
#     #     total_success_map = cursor.fetchone()    
#     #     print("total ", total_success_map)   
#     #     cursor.execute("""
#     #         select cs_uri_stem, count(cs_uri_stem) from download_log_2024 
#     #                     where date >= '2024-02-01'::date
#     #                     and date <= '2024-02-29'::date
#     #                     and x_edge_result_type <> 'Error'
#     #                     group by cs_uri_stem
#     #                     order by count desc
#     #                     limit 10
#     #         """)
#     #     count_by_key = cursor.fetchall()
#     #     cursor.execute("""
#     #         select 
#     #           (case 
#     #             when collection_id = '' then hist_collective||' '||hist_mission||' ('||hist_band||')'
#     #           else collection_shortname
#     #           end) as category, 
#     #           count(*) from download_log_2024 
#     #         where date >= '2024-02-01'::date
# 		# 							  and date <= '2024-02-29'::date
#     #                 and x_edge_result_type <> 'Error'
# 		# 							  group by category
# 		# 							  order by count desc
# 		# 							  limit 10
#     #         """)
#     #     count_by_collection = cursor.fetchall()
#     #     cursor.execute("""year
#     #         select collection_shortname, count(collection_shortname) from download_log_2024 
#     #                 where date >= '2024-02-01'::date
# 		# 							  and date <= '2024-02-29'::date
#     #                 and x_edge_result_type <> 'Error'
# 		# 							  and collection_id <> ''
# 		# 							  and area_type_id = 'map'start_date
# 		# 							  group by collection_shortname
# 		# 							  order by count desc
# 		# 							  limit 10
#     #         """)
#     #         select 
#     #           (case 
#     #             when hist_product = 'cog' and hist_file like '%_idx.zip' then 
#     #                    'historic imagery '||hist_type||'boundry shapefile'
#     #             else 'historic imagery '||hist_type||hist_product
#     #           end) as category, 
#     #           count(*) from download_log_2024 
#     #         where date >= '2024-02-01'::date
# 		# 							  and date <= '2024-02-29'::date
#     #                 and x_edge_result_type <> 'Error'
# 		# 							  and collection_id = ''
# 		# 							  group by category
# 		# 							  order by count desc
# 		# 							  limit 10
#     #     count_by_map = cursor.fetchall()
#     #     cursor.execute("""
#     #         select 
#     #           hist_collective||' '||hist_mission||' ('||hist_band||')' as historic_imagery_shortname, 
#     #           count(*) from download_log_2024 
#     #         where date >= '2024-02-01'::date
# 		# 							  and date <= '2024-02-29'::date
#     #                 and x_edge_result_type <> 'Error'
# 		# 							  and collection_id = ''
# 		# 							  group by historic_imagery_shortname
# 		# 							  order by count desc
# 		# 							  limit 10
#     #         """)
#     #     count_by_historic = cursor.fetchall()
#     #     cursor.execute("""
#     #         select 
#     #           (case 
#     #             when hist_product = 'cog' and hist_file like '%_idx.zip' then 
#     #                    'historic imagery '||hist_type||'boundry shapefile'
#     #             else 'historic imagery '||hist_type||hist_product
#     #           end) as category, 
#     #           count(*) from download_log_2024 
#     #         where date >= '2024-02-01'::date
# 		# 							  and date <= '2024-02-29'::date
#     #                 and x_edge_result_type <> 'Error'
# 		# 							  and collection_id = ''
# 		# 							  group by category
# 		# 							  order by count desc
# 		# 							  limit 10
#     #         """)
#     #     count_by_resource_type = cursor.fetchall()
#     #     cursor.execute("""
#     #         select 
#     #           x_edge_detailed_result_type,
#     #           (case 
#     #             when collection_id = '' then hist_collective||' '||hist_mission||' ('||hist_band||')'
#     #           else collection_shortname
#     #           end) as category, 
#     #           count(*) from download_log_2024 
#     #         where date >= '2024-02-01'::date
# 		# 							  and date <= '2024-02-29'::date
#     #                 and x_edge_result_type = 'Error'
# 		# 							  group by x_edge_detailed_result_type, category
# 		# 							  order by count desc
# 		# 							  limit 10
#     #         """)
#     #     count_by_error = cursor.fetchall()

#     # print("total downloads (raw query) completed in %s" % (time.time() - start_time))

#     all_log_classes = {
#         name[-4:]: clazz for name, clazz in inspect.getmembers(analytics.models, inspect.isclass) if clazz.__module__ == analytics.models.__name__
#     }
#     print(all_log_classes)
#     print(all_log_classes['2024'].objects.all().first())
#     default_end_date = datetime.now()
#     default_start_date = default_end_date.replace(day=1)
#     start_date = request.GET.get('start_date', default_start_date.strftime('%Y-%m-%d'))
#     end_date = request.GET.get('end_date', default_end_date.strftime('%Y-%m-%d'))
#     logs = None
#     try:
#         start_date = datetime.strptime(start_date, '%Y-%m-%d')
#         end_date = datetime.strptime(end_date, '%Y-%m-%d')
#         if start_date >= end_date:
#             raise Exception('start date must be before end date')
#         start_year = start_date.year
#         end_year = end_date.year
#         logs = all_log_classes[str(start_year)].objects.filter(date__gte=start_date.strftime('%Y-%m-%d'))
#         if start_year == end_year:
#             logs = logs.filter(date__lte=end_date.strftime('%Y-%m-%d'))
#         else:
#             year = start_year + 1
        
#             while year < end_year:
#                 logs = logs.union(all_log_classes[str(year)].objects.all())
#                 year += 1
#             logs = logs.union(all_log_classes[str(end_year)].objects.filter(date__lte=end_date.strftime('%Y-%m-%d')))
#         print(logs.count())    
#     except ValueError:
#         print('dates must be in the form YYYY-M-D') 
#         raise   
#     except Exception:
#         print('start date must be after end date')
#         raise
    
#     # logs = DownloadLog2024.objects.filter(date__gte=start_date).filter(date__lte=end_date)

#     # set aside dictionaries and variables for stats
#     total_downloads = 0
#     total_success_data = 0
#     total_success_map = 0
#     total_downloadable = len(no_downloads.keys())
#     count_by_error = {}
#     count_by_key = {}
#     count_by_collection = {}
#     count_by_historic = {}
#     count_by_map = {}
#     count_by_resource_type = {}

#     # start_time = time.time()
#     # for entry in logs:
#     #     total_downloads += 1
#     # print("just iterating through takes ", time.time() - start_time)
#     # total_downloads = 0

#     # start_time = time.time()
#     # for entry in logs:
#     #     total_downloads += 1
#     # print("just iterating through again takes ", time.time() - start_time)
#     # total_downloads = 0

#     start_time = time.time()
#     for entry in logs:
#         total_downloads += 1
#         if entry.x_edge_result_type != 'Error':
#             cus = entry.cs_uri_stem
#             count_by_key[cus] = count_by_key[cus] + 1 if cus in count_by_key.keys() else 1

#             if entry.collection_id != '':
#                 if entry.collection_id in no_downloads.keys():
#                     no_downloads.pop(str(entry.collection_id))

#                 sn = entry.collection_shortname
                
#                 if entry.area_type_id == 'map':
#                     # count by map
#                     total_success_map += 1
#                     count_by_map[sn] = count_by_map[sn] + 1 if sn in count_by_map.keys() else 1
#                 else:
#                     # count by collection
#                     total_success_map += 1
#                     count_by_collection[sn] = count_by_collection[sn] + 1 if sn in count_by_map.keys() else 1
                        

#                 # count by resource type

#                 ft = entry.file_type
#                 count_by_resource_type[ft] = count_by_resource_type[ft] + 1 if ft in count_by_resource_type.keys() else 1
#             else:
#                 total_success_data += 1
#                 historic_imagery_shortname = '%s %s (%s)' % (entry.hist_collective, entry.hist_mission, entry.hist_band)
#                 if historic_imagery_shortname not in count_by_collection.keys():
#                     count_by_collection[historic_imagery_shortname] = 1
#                 else:
#                     count_by_collection[historic_imagery_shortname] = count_by_collection[historic_imagery_shortname] + 1

#                 # (his = historic imagery shortname)
#                 his = '%s %s (%s)' % (entry.hist_collective, entry.hist_mission, entry.hist_band)
#                 # count by collection 
#                 count_by_collection[his] = count_by_collection[his] + 1 if his in count_by_collection.keys() else 1
#                 # count by historic
#                 count_by_historic[his] = count_by_historic[his] + 1 if his in count_by_historic.keys() else 1

#                 # (hit = historic imagery type)
#                 hit = 'historic imagery %s ' % (entry.hist_type)
#                 if entry.hist_product == 'cog' and '_idx.zip' in entry.hist_file:
#                     hit = hit + 'boundary shapefile'
#                 else:
#                     hit = hit + entry.hist_product
#                 count_by_resource_type[hit] = count_by_resource_type[hit] + 1 if hit in count_by_resource_type.keys() else 1

#         else:
#             shortname = entry.collection_shortname if (str(entry.collection_id) != '') else '%s %s (%s)' % (entry.hist_collective, entry.hist_mission, entry.hist_band) 
#             edrt = entry.x_edge_detailed_result_type
#             if edrt not in count_by_error.keys():
#                 count_by_error[edrt] = [shortname]
#             else:
#                 current = count_by_error[edrt]
#                 current.append(shortname)
#                 count_by_error[edrt] = current

#     print("main loop completed in %s", time.time() - start_time)
#     class Stats:
#         def __init__(self, total_downloads, total_success_data, total_success_map,
#         total_downloadable, count_by_error, count_by_key, count_by_collection,
#         count_by_historic, count_by_map, count_by_resource_type, no_downloads):
#             self.total_downloads = total_downloads
#             self.total_success_data = total_success_data
#             self.total_success_map = total_success_map
#             self.total_downloadable = total_downloadable
#             self.count_by_error = count_by_error
#             self.count_by_key = count_by_key
#             self.count_by_collection = count_by_collection
#             self.count_by_historic = count_by_historic
#             self.count_by_map = count_by_map
#             self.count_by_resource_type = count_by_resource_type
#             self.no_downloads = no_downloads
#             self.top_files = []
#             self.top_cbc = []
#             self.top_cbh = []
#             self.top_cbm = []
#             self.top_cbrt = []
#             self.no_downloads_num = 0
#             self.sorted_cbe = []
#         def __str__(self):
#             return json.dumps(self)
#         def toJSON(self):
#             return json.dumps(self, default=lambda o: o.__dict__, 
#                 sort_keys=True, indent=4)

    
#     download_stats = Stats(total_downloads, total_success_data, total_success_map,
#         total_downloadable, count_by_error, count_by_key, count_by_collection,
#         count_by_historic, count_by_map, count_by_resource_type, no_downloads)
    
#         # print compiled dictionaries
#     # sbj = ""
#     # txt = sbj + "   \t\r\n  \t\r\n"
#     # print('total downloads', total_downloads)
#     # txt += "total downloads %s   \t\r\n" % (total_downloads)
#     # print('successful data downloads', total_success_data)
#     # txt += "successful data downloads %s   \t\r\n" % (total_success_data)
#     # print('successful map downloads', total_success_map)
#     # txt += "successful map downloads %s   \t\r\n" % (total_success_map)
#     # print("-------------------------------------------")
#     # txt += "-------------------------------------------   \t\r\n"
#     # sorted_cbk = sorted(count_by_key.items(), key=lambda x: x[1], reverse=True)
#     # download_stats.top_files = sorted_cbk[0:10]
#     # print('top 10 successfully downloaded files :::')
#     # txt += "top 10 successfully downloaded files :::   \t\r\n"
#     # # for k in sorted_cbk[0:10]:
#     # for index, item in enumerate(download_stats.top_files):
#     #     print(type(item))
#     #     download_stats.top_files[index] = [item[0].split("/")[-1], item[1]]
#     #     # download_stats.top_files[index][0] = item[0].split("/")[-1]
#     #     print('Downloads:', item[1], download_stats.top_files[index][0])
#     #     txt += "Downloads: %s   %s   \t\r\n" % (item[1], download_stats.top_files[index][0])

#     # print(download_stats.__dict__)

#     # sorted_cbh = sorted(count_by_historic.items(), key=lambda x: x[1], reverse=True)
#     download_stats.top_cbc = sorted(count_by_collection.items(), key=lambda x: x[1], reverse=True)[0:10]    
#     download_stats.top_cbh = sorted(count_by_historic.items(), key=lambda x: x[1], reverse=True)[0:10] 
#     download_stats.top_cbm = sorted(count_by_map.items(), key=lambda x: x[1], reverse=True)[0:10]
#     download_stats.top_cbrt = sorted(count_by_resource_type.items(), key=lambda x: x[1], reverse=True)[0:10]  
#     download_stats.no_downloads_num = len(no_downloads)


#     # return HttpResponse(txt)
#     print("view finished in ", time.time() - start_time)

#     return render(request, 'stats.html', download_stats.__dict__) 

