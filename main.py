import sys, traceback
from web_classifier import WebClassifier
from rules import category_root


def main(account_key, t_es, t_ec, host):
    ''' Main function for running the whole program
    '''
    classifier = WebClassifier(account_key, t_es, t_ec, host)
    try:
        classifier.classify(category_root, 1.0)
    except Exception as e:
        print e
        # traceback.print_exc(file=sys.stdout)
    classifier.close()


if __name__ == '__main__':
    ACCOUNT_KEY = sys.argv[1]
    T_ES = float(sys.argv[2])
    T_EC = int(sys.argv[3])
    HOST = sys.argv[4]
    print 'input: %s %s %s %s' % (ACCOUNT_KEY, T_ES, T_EC, HOST)
    main(ACCOUNT_KEY, T_ES, T_EC, HOST)
