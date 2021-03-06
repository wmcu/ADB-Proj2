from search_web import Bing


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
        ''' Wrapper function that calls Bing search API with cache
            @query: list of keywords for query
            @return: (number of results, top-4 urls)
        '''
        return self.bing.search_web_cached(self.account_key, self.host, query)


    def close(self):
        ''' Safely close Bing object, as is requested by Bing class
            @return: None
        '''
        self.bing.close()


    def classify(self, category, especificity_c, path, results):
        ''' Main function for web database classification
            Also builds sample document urls for each category
            @category: the CategoryNode object, C
            @especificity_c: ESpecificity(host, C)
            @path: list[str], path from root category to current category
            @results: list[list[str]], all valid classification paths
            @return: None
        '''
        path.append(category.name)
        url_set = set()

        # compute e_coverage vector
        e_coverage_vector = {}
        sum_e_coverage = 0
        for sub_category_node in category.children:
            sub_category = sub_category_node.name
            probes = sub_category_node.queries
            e_coverage = 0
            for probe in probes:
                freq, top_urls = self.search_web(probe)
                e_coverage += freq
                url_set.update(top_urls)
            e_coverage_vector[sub_category] = e_coverage
            sum_e_coverage += e_coverage

        # compute e_especificity vector
        e_especificity_vector = {}
        for sub_category_node in category.children:
            sub_category = sub_category_node.name
            e_coverage = e_coverage_vector[sub_category]
            e_especificity = especificity_c * e_coverage / sum_e_coverage
            e_especificity_vector[sub_category] = e_especificity

            print 'Coverage for category "%s" is %s' % (sub_category, e_coverage)
            print 'Specificity for category "%s" is %s' % (sub_category, e_especificity)

        # check threshold and recurse
        push_down = False
        for sub_category_node in category.children:
            sub_category = sub_category_node.name
            e_especificity = e_especificity_vector[sub_category]
            e_coverage = e_coverage_vector[sub_category]
            if e_especificity < self.t_es or e_coverage < self.t_ec:
                continue
            # Recursively classify into sub_category
            push_down = True
            self.classify(sub_category_node, e_especificity, path, results)
            # Collect document sample urls of sub_category
            url_set |= sub_category_node.url_set

        # Attach document sample url to the category node object
        # for generating summary content
        category.url_set = url_set

        if not push_down:
            results.append(list(path))
        path.pop()
