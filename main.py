import sys, traceback
from web_classifier import WebClassifier
from rules import category_root
from dump_page import build_content_summary


def main(account_key, t_es, t_ec, host):
    ''' Main function for running the whole program
        @return: None
    '''
    # part 1: web database classification
    classifier = WebClassifier(account_key, t_es, t_ec, host)
    try:
        print '\nClassifying...\n'
        results = []
        classifier.classify(category_root, 1.0, [], results)
        print '\nClassification:\n'
        for result in results:
            print '/'.join(result)
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
    classifier.close()

    # part2: web database content summary
    print '\nBuilding content summary...',
    build_content_summary(host, category_root)
    print 'done.\n'


if __name__ == '__main__':
    ACCOUNT_KEY = sys.argv[1]
    T_ES = float(sys.argv[2])
    T_EC = int(sys.argv[3])
    HOST = sys.argv[4]
    print 'input: %s %s %s %s' % (ACCOUNT_KEY, T_ES, T_EC, HOST)
    main(ACCOUNT_KEY, T_ES, T_EC, HOST)
