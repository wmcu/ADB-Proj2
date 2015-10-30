from subprocess import Popen, PIPE


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


_cache_ = {}

def html_word_set_cached(url):
    if url in _cache_:
        return _cache_[url]

    result = html_word_set(url)
    _cache_[url] = result
    return result


if __name__ == '__main__':
    # dump_web_page('yahoo.com')
    # print html_word_set('http://pipes.yahoo.com/pipes/docs?doc=deprecated')
    print html_word_set('http://messenger.yahoo.com/win')
