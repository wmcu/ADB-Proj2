from subprocess import Popen, PIPE
from collections import defaultdict


def lynx_dump_generator(url):
    ''' Use lynx to dump html
        @return: every character before 'References'
    '''
    htmlfile = []
    try:
        # supress stderr
        lynxcmd = 'lynx --dump "%s" 2> /dev/null' % url
        htmlfile = Popen(lynxcmd, shell=True, stdout=PIPE).stdout
    except Exception as e:
        print '[%s]' % lynxcmd,
        print e

    for lin in htmlfile:
        line = lin.strip()
        if line == 'References':
            break
        for ch in line:
            yield ch
        yield ' '  # replace '\n' with ' '


def html_word_set(url):
    ''' Clean character stream from lynx_dump_generator
        text within brackets '[....]' is ignored
        character not in the English alphabet is word separator
        all character are converted to lowercase
        @return: a set of word
    '''
    recording = True
    wrotespace = True
    word_set = set()
    word_builder = []

    for ch in lynx_dump_generator(url):
        if recording:
            if ch == '[':
                recording = False
                if not wrotespace:
                    word = ''.join(word_builder)
                    word_set.add(word.lower())
                    word_builder = []
                    wrotespace = True
                continue
            else:
                if ch.isalpha():
                    word_builder.append(ch)
                    wrotespace = False
                else:
                    if not wrotespace:
                        word = ''.join(word_builder)
                        word_set.add(word.lower())
                        word_builder = []
                        wrotespace = True
        else:
            if ch == ']':
                recording = True

    return word_set


# global variable
# cache: (url, word_set) pairs
_cache_ = {}


def html_word_set_cached(url):
    ''' Get word set from url with cache
        Call html_word_set in cache miss
        @return: a set of word
    '''
    global _cache_

    if url in _cache_:
        return _cache_[url]

    result = html_word_set(url)
    _cache_[url] = result
    return result


def build_content_summary(host, category_node):
    ''' Generate content summary of @host from doc urls in @category_node
        Side effect: write content summary txt files to `cwd`
        @return: None
    '''
    if not category_node.url_set:
        return

    # recusively build content summary for sub category
    for sub_category_node in category_node.children:
        build_content_summary(host, sub_category_node)

    # count document frequency
    word_map = defaultdict(int)
    for url in category_node.url_set:
        # update document frequency
        tmp_set = html_word_set_cached(url)
        for word in tmp_set:
            word_map[word] += 1

    # sort (word, df) pairs
    word_freq_pairs = [(word, word_map[word]) for word in word_map]
    word_freq_pairs.sort()

    # write to file
    file_name = '%s-%s.txt' % (category_node.name, host)
    with open(file_name, 'w') as fout:
        for pair in word_freq_pairs:
            print >>fout, '%s#%s' % pair


if __name__ == '__main__':
    # dump_web_page('yahoo.com')
    # print html_word_set('http://pipes.yahoo.com/pipes/docs?doc=deprecated')
    print html_word_set('http://messenger.yahoo.com/win')
