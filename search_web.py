import urllib2
import base64
import json
import cPickle


def search_web(account_key, host, query_list):
    ''' Call Bing search API
        @return: (number of results, top-4 urls)
    '''
    # Format API url
    bing_api_root = 'https://api.datamarket.azure.com/Bing/SearchWeb/v1'
    bing_url_prefix = bing_api_root + '/Composite?Query='
    pre_handled_query = '+'.join(query_list)
    handled_query = '%27' + 'site%3a' + host + '%20' + pre_handled_query + '%27'
    top = '$top=4'
    encode_format = '$format=json'
    final_url = bing_url_prefix + handled_query + '&' + top + '&' + encode_format

    # Call API
    account_key_enc = base64.b64encode(account_key + ':' + account_key)
    headers = {'Authorization': 'Basic ' + account_key_enc}
    request = urllib2.Request(final_url, headers=headers)
    response = urllib2.urlopen(request)
    content = response.read()
    json_content = json.loads(content)

    # Parse json result
    web_result = json_content['d']['results'][0]
    result_number = long(web_result['WebTotal'])
    results = web_result['Web']
    top_pages_url = [x['Url'] for x in results[:4]]

    return result_number, top_pages_url


class Bing(object):
    ''' Wrapper calss for Bing search API, with cache
    '''
    def __init__(self):
        ''' Initialize cache by loading pkl file
        '''
        self._search_cache = {}
        self.search_cache_pkl = 'search_cache.pkl'

        try:
            with open(self.search_cache_pkl, 'rb') as fin:
                self._search_cache = cPickle.load(fin)
        except Exception as e:
            pass
            # print e


    def search_web_cached(self, account_key, host, query_list):
        ''' Call Bing search API
            Make real API call only in cache miss
            @return: (number of results, top-4 urls)
        '''
        cache_key = (host, tuple(query_list))

        if cache_key in self._search_cache:
            return self._search_cache[cache_key]

        result = search_web(account_key, host, query_list)
        self._search_cache[cache_key] = result

        return result


    def close(self):
        ''' Save cache to pkl file
            This method must be invoked before disposing object
            Otherwise the cache data would lost
        '''
        try:
            with open(self.search_cache_pkl, 'wb') as fout:
                cPickle.dump(self._search_cache, fout)
        except Exception as e:
            pass
            # print e


if __name__ == '__main__':

    print search_web(
        '/Hg13bNu9hmSAQfQXlpIdsEDEq+h2Zt03GHnlZ2EFKk',
        'health.com',
        ['fitness']
    )

    bing = Bing()
    print bing.search_web_cached(
        '/Hg13bNu9hmSAQfQXlpIdsEDEq+h2Zt03GHnlZ2EFKk',
        'health.com',
        ['fitness']
    )

    print bing.search_web_cached(
        '/Hg13bNu9hmSAQfQXlpIdsEDEq+h2Zt03GHnlZ2EFKk',
        'health.com',
        ['workout']
    )

    bing.close()

