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
    ...
