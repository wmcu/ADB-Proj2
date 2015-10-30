import traceback
from rules import probes_map
from search_web import Bing
from dump_page import html_word_set_cached
from collections import defaultdict


class WebClassifier(object):
    ''' Main class for web database classification
        Also builds content summary for each category
    '''
    def __init__(self, account_key, t_es, t_ec, host):
        self.account_key = account_key
        self.bing = Bing()
        self.host = host
        self.t_es = t_es
        self.t_ec = t_ec


    def search_web(self, query):
        ''' Helper function that calls Bing search API with cache
        '''
        return self.bing.search_web_cached(self.account_key, self.host, query)


    def close(self):
        ''' Safely close Bing object, as is requested by Bing class
        '''
        self.bing.close()


    def classify(self, category, especify_category):
        ''' Main function for web database classification
            Also builds content summary for each category
        '''
        result = [category.name]
        url_set = set()

        # if leaf node, return early
        if len(category.children) == 0:
            return result, url_set

        print '\nClassifying...\n'

        # compute e_coverage vector
        e_coverage_vector = {}
        sum_e_coverage = 0
        for sub_category_node in category.children:
            sub_category = sub_category_node.name
            probes = probes_map[sub_category]
            e_coverage = 0
            for probe in probes:
                freq, top_urls = self.search_web(probe)
                e_coverage += freq
                url_set.update(top_urls)
            e_coverage_vector[sub_category] = e_coverage
            sum_e_coverage += e_coverage

        # compute e_specify_vector
        e_specify_vector = {}
        for sub_category_node in category.children:
            sub_category = sub_category_node.name
            e_especify_num = especify_category * e_coverage_vector[sub_category]
            e_specify_vector[sub_category] = e_especify_num / sum_e_coverage

            print 'Coverage for category "%s" is %s' % (sub_category, e_coverage_vector[sub_category])
            print 'Specificity for category "%s" is %s' % (sub_category, e_specify_vector[sub_category])

        # check threshold
        for sub_category_node in category.children:
            sub_category = sub_category_node.name
            e_specify = e_specify_vector[sub_category]
            e_coverage = e_coverage_vector[sub_category]
            if e_specify >= self.t_es and e_coverage >= self.t_ec:
                sub_result, sub_url_set = self.classify(sub_category_node, e_specify)
                result += sub_result
                url_set |= sub_url_set

        # print classification result
        print '\nClassification:\n'
        print '/'.join(result)

        # Generate sample file
        self.generate_sample_from_urls(category.name, url_set)

        return result, url_set


    def generate_sample_from_urls(self, category_name, url_set):
        ''' Generate sample file from set of top urls
        '''
        # count document frequency
        word_map = defaultdict(int)
        for url in url_set:
            # update document frequency
            tmp_set = html_word_set_cached(url)
            for word in tmp_set:
                word_map[word] += 1

        # sort (word, df) pairs
        word_freq_pairs = [(word, word_map[word]) for word in word_map]
        word_freq_pairs.sort()

        # write to file
        file_name = '%s-%s.txt' % (category_name, self.host)
        with open(file_name, 'w') as fout:
            for pair in word_freq_pairs:
                print >>fout, '%s#%s' % pair
