__author__ = 'youhanwang, MengWang'

import urllib2
import base64
import json
import cPickle


def search_web(account_key, host, query_list):
    """Call Bing search API
    return: (number of results, final_url)
    """
    bing_api_root = 'https://api.datamarket.azure.com/Bing/SearchWeb/v1'
    bing_url_prefix = bing_api_root + '/Composite?Query='
    pre_handled_query = '+'.join(query_list)

    handled_query = '%27' + 'site%3a' + host + '%20' + pre_handled_query + '%27'
    top = '$top=1'
    encode_format = '$format=json'
    final_url = bing_url_prefix + handled_query + '&' + top + '&' + encode_format

    account_key_enc = base64.b64encode(account_key + ':' + account_key)
    headers = {'Authorization': 'Basic ' + account_key_enc}
    request = urllib2.Request(final_url, headers=headers)
    response = urllib2.urlopen(request)
    content = response.read()
    json_content = json.loads(content)
    result_number = json_content['d']['results'][0]['WebTotal']

    return result_number, final_url


class Bing:
    ''' search_web with cache
    '''
    def __init__(self):
        self._search_cache = {}
        try:
            fin = open('search_cache.pkl', 'rb')
            tmp = cPickle.load(fin)
            fin.close()
            self._search_cache = tmp
        except Exception as e:
            pass
            # print e

    def search_web_cached(self, account_key, host, query_list):
        cache_key = (host, tuple(query_list))

        if cache_key in self._search_cache:
            return self._search_cache[cache_key]

        result = search_web(account_key, host, query_list)
        self._search_cache[cache_key] = result

        return result

    def close(self):
        try:
            fout = open('search_cache.pkl', 'wb')
            cPickle.dump(self._search_cache, fout)
            fout.close()
        except Exception as e:
            pass
            # print e


if __name__ == '__main__':
    bing = Bing()
    print bing.search_web_cached(
        '/Hg13bNu9hmSAQfQXlpIdsEDEq+h2Zt03GHnlZ2EFKk',
        'health.com',
        ['fitness']
    )

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

