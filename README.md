# ADB-Proj2
Project2 for ADB course

by: Meng Wang (mw2972), Youhan Wang (yw2663)

1. File structue
    main.py - main script; entry point for whole program
    rules.py - load asset files and catrgory tree structure
    asset/ - contains the txt files of queries, as provided in course webpage
    search_web.py - wrappers of Bing search API invoking
    web_classifier.py - contains web database classification algorithm
    dump_page.py - contains content summary generation algorithm
    README.md - readme file (the one your are looking at)

2. How to run
    Usage:

    $ python main.py <BING_ACCOUNT_KEY> <t_es> <t_ec> <host>

2. Data structure
    The most important data structure is class CategoryNode. Since categories are natually a tree structure, we design this tree node structure to maintain all data of categories. This class contains queries, document sample urls, and sub categories of a category. When the main.py imports global variable `category_root' from rules.py, the queries are loaded from four txt files assets/. Then the `classify' method of WebClassifier class will take CategoryNode as input parameter and use those queries for classification. Meanwhile, the document sample urls of each category is saved in the CategoryNode. So that `build_content_summary' method can use those doc sample urls to generate content summary.

3. Main work flow
    In main.py, a global variable `category_root' is imported from rules.py. `category_root' was iniatilized on import and contains category structure with all queries. Then four command line arguments are retrieved and passed into `main' function. In `main' function, the given host is first classified with `classify' method of `WebClassifier' class against given category structure. then `build_content_summary' function is invoked to generate content summary for given host, using the sample document urls collected in classification step.

4. Web database classification algorithm
    In each run of the program, the host (database, D) and t_es, t_ec are fixed, and are passed to __init__ method of `WebClassifier' class. So we ommit D in the folowing algorithm analysis.
    This algorithm is implemented in `classify' method of `WebClassifier' class. The method takes two arguments: the CategoryNode object C, and ESpecificity(C). The `classify' method returns a list of category names which the host has been classified to, which looks like `[Root, Sport, Soccer]'; it also returns a set of document set urls for C.
    First, the input category C is checked: if it has no subcategory, then simply return [C]
    Then, compute ECoverage vector of C, which contains ECoverage of each sub category C_i of C. For C_i, the call Bing search API with every query, and sum up the number of total hits as ECoverage(C_i). Meanwhile, the top-4 urls of each query are added to the sample document url set of C (not C_i).
    Next, compute ESpecificity vector of C, which contains ESpecificity of each sub category C_i of C. By definition, ESpecificity(C_i) = ESpecificity(C) * ECoverage(C_i) / sum(ECoverage vector).
    Now with ESpecificity and ECoverage, check them against t_es, t_ec. For C_i that meets the thresholds, recursively call classify(C_i, ESpecificity(C_i)). Then the result returned by recusive call is concatenated with name of C; the document sample urls are unioned into doc sample urls of C.
    Finally, the doc sample urls are attached to CategoryNode C, make it ready for generating content summary in part2.

5. Content summary generation algorithm
    As descibed in section 4, the doc sample url set of each category is already collected in classification. Now `build_content_summary' method is invoked to generate content summary files. It takes two arguments: the host, and the CategoryNode tree. It traverse the tree to generate content summary for each category, according to their doc sample urls. Since I use `set' data structure to keep all urls, duplications are removed automatically.
    For each url, `html_word_set' function is invoked: lynx command is invoked to retrieve plain text webpages contents. Then the text are cleaned as described in course website, words splitted and kept in a set. Since one url may be dumped more than once, a `html_word_set_cached' is introduced, which is a wrapper of `html_word_set' with a cache.
    For each category, after all its doc sample word set are dumped, the document frequency of each word is computed. Then all (word, document frequency) pairs are sorted by word and written to file.

6. BING ACCOUNT KEY
    /Hg13bNu9hmSAQfQXlpIdsEDEq+h2Zt03GHnlZ2EFKk

7. Other findings
    When collecting documents on `yahoo.com', two 'bad' urls are found. One of them cannot even be opened by normal web browser like Chrome. Another url is redirected to https connection, where lynx reports SSL error. For these error urls, I make sure `html_word_set' function returns empty set.
