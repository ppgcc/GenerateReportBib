from pybtex.database import parse_file

bib_data = parse_file('references.bib')
LANGUAGE = 'eng'

assert LANGUAGE in ['eng', 'pt']
if LANGUAGE == 'eng':
    MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
elif LANGUAGE == 'pt':
    MONTHS = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']


REQ = {
    'article': {'title', 'author', 'journal', 'volume', 'year', 'pages'},
    'inproceedings': {'title', 'author', 'booktitle', 'pages', 'year'},
    'techreport': {'title', 'author', 'numpages', 'institution', 'year', 'type'},
    'incollection': {'title', 'author', 'year', 'booktitle', 'publisher'},
    'inbook': {'title', 'author', 'year', 'pages', 'publisher', 'chapter'},
    'booklet': {'title', 'author', 'howpublished', 'address', 'year', 'numpages'},
    'misc': {'title', 'author', 'url', 'urlaccessdate'},
    'mastersthesis': {'title', 'author', 'numpages', 'school', 'year', 'type'},
    'phdthesis': {'title', 'author', 'numpages', 'school', 'year', 'type'},
    'book': {'author', 'title', 'publisher', 'year', 'numpages'}
}


def check(bib):
    fields = set(bib.fields.keys() + bib.persons.keys())
    if bib.type not in REQ.keys():
        raise Exception('Type %s not implemented' % bib.type)
        
    req = REQ[bib.type].difference(fields)
    if bib.type == 'article' and 'year' in fields:
        year_check = check_article_year(bib.fields['year'])
        if not year_check:
            print(bib.key + ': Failed {Month year} check') 
        
    return req

def check_article_year(year):
    year = year.split()
    try:
        month, year = year[0], year[1]
        MONTHS.index(month)
        int(year)
    except:
        return False

    return True
        

for entry in bib_data.entries:
    bib = bib_data.entries[entry]

    req = check(bib)
    
    if len(req) > 0:
        print(entry, ': ', bib.fields['title'], ' --- ', req)
        #print(bib)
        #print(fields)



