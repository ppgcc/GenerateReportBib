import re
import os
import shlex
import json
import shutil
import nltk

from langdetect import detect
from pathlib import Path
from datetime import datetime
from datetime import date
from pybtex.database import parse_file, BibliographyDataError, Entry
from pybtex.database.input.bibtex import UndefinedMacro
from pybtex.scanner import TokenRequired
from pybtex.richtext import Text, Tag
from nltk.corpus import stopwords

now = datetime.now()
label_date = str(date.today()) + now.strftime("_%H-%M-%S")

con_file = open("config.json")
config = json.load(con_file)
con_file.close()
LANGUAGE = config['LANGUAGE']
TYPE_REFERENCES = config['TYPE_REFERENCES']
NAME_FILE = config['NAME-FILE'] + ".bib"
NAME_FILE_OUTPUT_REPORT_MD = config['NAME-FILE'] +"_Report_" + label_date + ".md"
NAME_FILE_OUTPUT_REPORT_HTML = config['NAME-FILE'] +"_Report_" + label_date + ".html"

NAME_FILE_OUTPUT_BIB = config['NAME-FILE'] + "_" + label_date + ".bib"


#Stopwords for capitalization
#nltk.download('stopwords')
LIST_STOPWORDS_ENGLISH = stopwords.words('english')
LIST_STOPWORDS_ENGLISH.append('st')
LIST_STOPWORDS_ENGLISH.append('nd')
LIST_STOPWORDS_ENGLISH.append('rd')

LIST_STOPWORDS_PORTUGUESE = stopwords.words('portuguese')

#Create directories
path_current = os.getcwd() # Current directory

path_bib_original = path_current+"\\OriginalBIB\\"
Path(path_bib_original).mkdir(parents=True, exist_ok=True)

path_reports = path_current+"\\GenerateReports\\"
Path(path_reports).mkdir(parents=True, exist_ok=True)

path_bib = path_current+"/GenerateBIB/"
Path(path_bib).mkdir(parents=True, exist_ok=True)

## Load configuration
def main():

    file = open("results.txt","w+")

    lineHeader1 = "# References Report: " + str(label_date) + '\r'
    lineHeader2 = "## - Configurations: _Bib File:_ **"+ NAME_FILE +"** / _Language:_ **"+ LANGUAGE +"** / _Type References:_ **"+ TYPE_REFERENCES +"**\r\n"
    file.write(lineHeader1)
    file.write(lineHeader2)

    # ===========================================================
    # If repeated bibliograhpy entry or others erros
    msg_erros = ''
    stop = True
    read_error = False
    pass_language = False

    count = 0
    while stop == True:
        try:

            assert LANGUAGE in ['english', 'portuguese']
            pass_language == True
            assert TYPE_REFERENCES in ['apa', 'num-alpha']
            if os.path.exists("refer_find_errors_generate.bib") == False:
                shutil.copyfile(path_bib_original+config['NAME-FILE']+'.bib', 'refer_find_errors_generate.bib')

            bib_data = parse_file('refer_find_errors_generate.bib')
            stop = False
        except FileNotFoundError as identifier:
            read_error = True
            msg_erros += '- ## The file name defined in the [NAME-FILE] parameter of the `config.json` file was not found in the bib files folder. '
            msg_erros += 'Check if it is actually in the folder (OriginalBIB) or if the file name was spelled correctly in the parameter. '
            msg_erros += 'Remember to NOT specify the extension (.bib) in the config.json file : ' + str(identifier) + '\r'
            stop = False

        except AssertionError as identifier:
            read_error = True

            if pass_language == True:
                msg_erros += '- ## The value defined in the `[TYPE_REFERENCES]` parameter of the `config.json` file is not valid. '
                msg_erros += 'Valid values: [`apa` or `num-alpha`].' + str(identifier) + '\r'
            else:
                msg_erros += '- ## The value defined in the `[LANGUAGE]` parameter of the `config.json` file is not valid. '
                msg_erros += 'Valid values: [`english` or `portuguese`].' + str(identifier) + '\r'

            stop = False
        except BibliographyDataError as identifier:
            read_error = True

            count+=1
            msg_erros += '- ## ' + str(identifier) + '\r'
            tag_rep = str(identifier).split(':')

            #input file
            fin = open("refer_find_errors_generate.bib", "rt")
            contents = fin.read().replace(str(tag_rep[1]).strip(), str(tag_rep[1]).strip()+str(count), count)
            fin.close()

            fin = open("refer_find_errors_generate.bib", "w+")
            fin.write(contents)
            fin.close()

        except UndefinedMacro as identifier:
            read_error = True
            erro = identifier.args[0]
            msg_erros += '- ## ' + str(identifier) + '\r'

            #input file
            fin = open("refer_find_errors_generate.bib", "rt")
            contents = fin.read().replace(erro, 'JAN')
            fin.close()

            fin = open("refer_find_errors_generate.bib", "w+")
            fin.write(contents)
            fin.close()

        except TokenRequired as identifier:
            read_error = True
            erro = identifier.args[0]
            value_new = ''

            msg_erros += '## - ' + str(identifier) + '\r'

            #input file
            fin = open("refer_find_errors_generate.bib", "rt")
            contents = fin.read().replace(erro, value_new)
            fin.close()

            fin = open("refer_find_errors_generate.bib", "w+")
            fin.write(contents)
            fin.close()
            stop = False

    if os.path.exists("refer_find_errors_generate.bib"):
        os.remove("refer_find_errors_generate.bib")


    # ===========================================================

    if read_error == True:
        line1 = '# Error reading your .bib file!\r\n'
        line2 = '### Errors may be related:\r'
        line3 = '- the label of repeated references. Repeated entries will be listed below. '
        line4 = 'Check the labels (tags) used before continuing to run the report.\r'
        line5 = '- information for month={WRONG}. This field must always be filled in English (even if its volume is in Portuguese), '
        line6 = 'nor can it be empty. '
        line7 = '(_Accepted formats: [Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec]_)\r\n'
        line8 = '# Errors found:\r'

        line9 = '#### *Warning:* Correct repeated entries or month information in your original .bib file. '
        line10 = 'Afterwards, run this script again to generate the error report. \r'
        file.write(line1)
        file.write(line2)
        file.write(line3)
        file.write(line4)
        file.write(line5)
        file.write(line6)
        file.write(line7)
        file.write(line8)
        file.write(msg_erros+'\r\n')
        file.write(line9)
        file.write(line10)

    else:
        MONTHS_ENG_VALID = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        MONTHS_PORT_VALID = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

        assert LANGUAGE in ['english', 'portuguese']
        if LANGUAGE == 'english' and TYPE_REFERENCES == 'apa':
            MONTHS = ['Jan,', 'Feb,', 'Mar,', 'Apr,', 'May,', 'Jun,', 'Jul,', 'Aug,', 'Sep,', 'Oct,', 'Nov,', 'Dec,']

        elif LANGUAGE == 'english' and TYPE_REFERENCES == 'num-alpha':
            MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        elif LANGUAGE == 'portuguese' and TYPE_REFERENCES == 'apa':
            MONTHS = ['Jan,', 'Fev,', 'Mar,', 'Abr,', 'Mai,', 'Jun,', 'Jul,', 'Ago,', 'Set,', 'Out,', 'Nov,', 'Dez,']

        elif LANGUAGE == 'portuguese' and TYPE_REFERENCES == 'num-alpha':
            MONTHS = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

        assert TYPE_REFERENCES in ['apa', 'num-alpha']
        if TYPE_REFERENCES == 'num-alpha':
            REQ = {
                'book': {'author', 'title', 'publisher', 'year', 'numpages'},
                'article': {'title', 'author', 'journal', 'volume', 'year', 'month', 'pages'},
                'inproceedings': {'title', 'author', 'booktitle', 'pages', 'year'},
                'conference': {'title', 'author', 'booktitle', 'pages', 'year'},
                'proceedings': {'title', 'author', 'booktitle', 'pages', 'year'},
                'mastersthesis': {'title', 'author', 'numpages', 'school', 'year'},
                'phdthesis': {'title', 'author', 'numpages', 'school', 'year'},
                'techreport': {'title', 'author', 'numpages', 'institution', 'year'},
                'misc': {'title', 'author', 'url', 'urlaccessdate'},
                'booklet': {'title', 'author', 'howpublished', 'address', 'year', 'numpages'},
                'inbook': {'title', 'author', 'year', 'pages', 'publisher', 'chapter'},
                'incollection': {'title', 'author', 'year', 'booktitle', 'publisher'}
            }
        elif TYPE_REFERENCES == 'apa':
            REQ = {
                'book': {'title', 'author', 'publisher', 'year', 'address'},
                'article': {'title', 'author', 'year', 'journal', 'pages', 'volume'},
                'inproceedings': {'title', 'author', 'booktitle', 'pages', 'address', 'organization', 'year'},
                'conference': {'title', 'author', 'booktitle', 'pages', 'address', 'organization', 'year'},
                'proceedings': {'title', 'author', 'booktitle', 'pages', 'year'},
                'mastersthesis': {'title', 'author', 'year', 'school', 'address'},
                'phdthesis': {'title', 'author', 'year', 'school', 'address'},
                'techreport': {'title', 'author', 'institution', 'year', 'type'},
                'misc': {'title', 'author', 'year', 'note', 'howpublished'},
                'booklet': {'title', 'author', 'howpublished', 'address', 'year'},
                'inbook': {'title', 'author', 'year', 'pages', 'publisher', 'address', 'chapter'},
                'incollection': {'title', 'author', 'year', 'booktitle', 'publisher', 'volume', 'pages', 'edition'}
            }

        bib_data = parse_file(path_bib_original+NAME_FILE)
        ##

        line1 = '| Error | Type |Tag | Title | Warning |' + '\r'
        line2 = '|-:|:---:|:---:|:---:|:------:|' + '\r'
        file.write(line1)
        file.write(line2)

        count=0
        tag_inv_global = False
        for entry in bib_data.entries:
            bib = bib_data.entries[entry]
            #print('entry: ============ ', entry)
            msg = check(bib, REQ, MONTHS, TYPE_REFERENCES)
            tag_inv, bib = regenerate_bib(bib, REQ)

            if tag_inv == False:
                bib_data.entries[entry] = bib
            else:
                tag_inv_global = True

            if len(msg) > 0:
                count+=1
                line = '| ' + str(count) +' |@'+ bib.type + '| {' + str(entry) + '} |' + str(bib.fields['title']) + ' | ' + msg + ' | ' + '\r'
                file.write(line)

        if tag_inv_global == False:
            file_bib = open(path_bib+NAME_FILE_OUTPUT_BIB,"w+", encoding="utf-8")
            file_bib.write(bib_data.to_string('bibtex'))
            file_bib.close()

            if LANGUAGE == 'portuguese':
                fin = open(path_bib+NAME_FILE_OUTPUT_BIB, "rt+")
                contents = ''
                for index, month in enumerate(MONTHS_ENG_VALID):
                    month_pt = MONTHS_PORT_VALID[index].upper()
                    contents += fin.read().replace(month, month_pt)

                fin.close()

                fin = open(path_bib+NAME_FILE_OUTPUT_BIB, "w+")
                fin.write(contents)
                fin.close()

        if count != 0:
            lineFooter1 = "# _Total references:_ **" + str(len(bib_data.entries)) + "** / _References with errors:_ **" + str(count) +"**\r\n"
            lineFooter2 = '## _Check the errors shown below_ \r'
            lineFooter3 = '- After correcting them, run the script again to ensure no new inconsistencies (or not).\r\n'
            file.write(lineFooter1)
            file.write(lineFooter2)
            file.write(lineFooter3)

            if tag_inv_global == True:
                line5 = '## **New .bib file was not generated!** _Invalid tags have been identified in your .bib_.\r'
                line6 = '- In order to generate a .bib with the missing fields, first you need to correct these tags in your '
                line7 = 'original .bib and only after running the script again.\r'
                line8 = '- In the column _Warning_ you will enter which of the references is with: _**Type not implemented**_\r'
                line9 = '- Valid tags: _@book, @article, @inproceedings, @proceedings, @mastersthesis, @phdthesis, '
                line10 = '@techreport, @misc, @booklet, @inbook, @incollection_.'
                file.write(line5)
                file.write(line6)
                file.write(line7)
                file.write(line8)
                file.write(line9)
                file.write(line10)

        else:
            lineCongrat1 = '# Congratulations! \r\n'
            lineCongrat2 = '## - No errors were identified in the fields. However, it is still necessary to check the standardization of your references, which this script does not guarantee.'
            file.write(lineCongrat1)
            file.write(lineCongrat2)

    file.close()

    shutil.copyfile("results.txt", NAME_FILE_OUTPUT_REPORT_MD)

    command = "grip "+NAME_FILE_OUTPUT_REPORT_MD+" --export "+NAME_FILE_OUTPUT_REPORT_HTML
    os.system(command)

    del_html = False
    file_html = open(NAME_FILE_OUTPUT_REPORT_HTML, "rt")
    contents = file_html.read()
    if '500 Internal Server Error' in contents:
        del_html = True
    file_html.close()

    if del_html == True:
        shutil.copyfile(NAME_FILE_OUTPUT_REPORT_MD, path_reports+NAME_FILE_OUTPUT_REPORT_MD)
    else:
        shutil.copyfile(NAME_FILE_OUTPUT_REPORT_HTML, path_reports+NAME_FILE_OUTPUT_REPORT_HTML)

    if os.path.exists("results.txt"):
        os.remove("results.txt")
    if os.path.exists(NAME_FILE_OUTPUT_REPORT_MD):
        os.remove(NAME_FILE_OUTPUT_REPORT_MD)
    if os.path.exists(NAME_FILE_OUTPUT_REPORT_HTML):
        os.remove(NAME_FILE_OUTPUT_REPORT_HTML)


def regenerate_bib(bib, REQ):
    tag_inv = False
    if bib.type not in REQ.keys():
        tag_inv = True
    else:
        list_fields_keys = [field_key.lower() for field_key in bib.fields.keys()]
        list_fields_persons = [field_person.lower() for field_person in bib.persons.keys()]
        fields = set(list_fields_keys + list_fields_persons)

        missing = REQ[bib.type].difference(fields)

        for value in missing:
            bib.fields[value] = 'MISSING'

    return tag_inv, bib

##
def check(bib, req, months, type_references):
    list_fields_keys = [field_key.lower() for field_key in bib.fields.keys()]
    list_fields_persons = [field_person.lower() for field_person in bib.persons.keys()]
    fields = set(list_fields_keys + list_fields_persons)
    msg = ''

    if bib.type not in req.keys():
        msg = 'Type not implemented: ' + bib.type
        #req = {bib.type}
    else:
        if type_references == 'apa':
            if bib.type == 'article' and 'year' in fields:
                year_month_check = check_article_year_month(bib.fields['year'], months, type_references)
                if not year_month_check:
                    msg += 'Failed Month and Year: year={Mon, Year} check'
        if type_references == 'num-alpha':
            if bib.type == 'article' and 'month' in fields:
                month_check = check_article_year_month(bib.fields['month'], months, type_references)
                if not month_check:
                    msg += 'Failed Month month={ Mon } check'

        missing = req[bib.type].difference(fields)
        if len(missing) > 0:
            if len(msg) > 0:
                msg += ', Missing: ' + str(missing)
            else:
                msg = 'Missing: ' +str(missing)

        if bib.type == 'book' or bib.type == 'inbook':
            exist = 'publisher' in missing
            if exist == False:
                phrase = bib.fields['publisher']
                msg = find_year(phrase, msg)
                publisher_capitalize = check_parentheses_and_capitalize(phrase)

                if publisher_capitalize == True:
                    if len(msg) > 0:
                        msg += ', Field { publisher } is not capitalized'
                    else:
                        msg = 'Field { publisher } is not capitalized'

        if bib.type == 'article':
            exist = 'journal' in missing
            if exist == False:
                phrase = bib.fields['journal']
                msg = find_year(phrase, msg)
                journal_capitalize = check_parentheses_and_capitalize(phrase)

                if journal_capitalize == True:
                    if len(msg) > 0:
                        msg += ', Field { journal } is not capitalized'
                    else:
                        msg = 'Field { journal } is not capitalized'

        if bib.type == 'inproceedings' or bib.type == 'proceedings' or bib.type == 'incollection' or bib.type == 'conference':
            exist = 'booktitle' in missing
            if exist == False:
                phrase = bib.fields['booktitle']
                msg = find_year(phrase, msg)
                booktitle_capitalize = check_parentheses_and_capitalize(phrase)

                if booktitle_capitalize == True:
                    if len(msg) > 0:
                        msg += ', Field { booktitle } is not capitalized'
                    else:
                        msg = 'Field { booktitle } is not capitalized'

        if bib.type == 'mastherthesis' or bib.type == 'phdthesis':
            exist = 'school' in missing
            if exist == False:
                phrase = bib.fields['school']
                msg = find_year(phrase, msg)
                school_capitalize = check_parentheses_and_capitalize(phrase)

                if school_capitalize == True:
                    if len(msg) > 0:
                        msg += ', Field { school } is not capitalized'
                    else:
                        msg = 'Field { school } is not capitalized'

        if bib.type == 'techreport':
            exist = 'institution' in missing
            if exist == False:
                phrase = bib.fields['institution']
                msg = find_year(phrase, msg)
                institution_capitalize = check_parentheses_and_capitalize(phrase)

                if institution_capitalize == True:
                    if len(msg) > 0:
                        msg += ', Field { institution } is not capitalized'
                    else:
                        msg = 'Field { institution } is not capitalized'

    return msg

def find_year(phrase, msg):
    result = re.findall(re.compile('.*([1-3][0-9]{3})'), phrase)
    if len(result) > 0:
        if len(msg) > 0:
            msg += ', The { journal } field takes no YEAR information:  '+ str(result) +' remove'
        else:
            msg = 'The { journal } field takes no YEAR information:  '+ str(result) +' remove'

    return msg

def check_parentheses_and_capitalize(phrase):
    language = detect(phrase)

    #remove parenthesis
    phrase = re.sub(r"\((.*?)\)", ' ', phrase)

    words = phrase.split()

    uncapitalized = False
    if language == 'en':
        for word in words:
            if word not in LIST_STOPWORDS_ENGLISH:
                if "-" in word:
                    words_hifen = word.split('-')
                    word = words_hifen[0]
                if word.isupper() == False:
                    if word != word.capitalize():
                        uncapitalized == True
                        break

    elif language == 'pt':
        for word in words:
            if word not in LIST_STOPWORDS_PORTUGUESE:
                if "-" in word:
                    words_hifen = word.split('-')
                    word = words_hifen[0]
                if word.isupper() == False:
                    if word != word.capitalize():
                        uncapitalized == True
                        break

    return uncapitalized

def check_article_year_month(fields, months, type_references):
    fields = fields.split()

    if type_references == "apa":
        try:
            month, year = fields[0][-4:], fields[1]
            months.index(month)
            int(year)
        except:
            return False
    #elif type_references == "num-alpha":
    #    month, year = fields[0][-3:], fields[1]

    return True

if __name__ == "__main__":
    main()
