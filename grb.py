import re
import os
import shlex
import json
import shutil
import nltk
import argparse

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

#Stopwords for capitalization
#nltk.download('stopwords')
LIST_STOPWORDS_ENGLISH = stopwords.words('english')
LIST_STOPWORDS_ENGLISH.append('st')
LIST_STOPWORDS_ENGLISH.append('nd')
LIST_STOPWORDS_ENGLISH.append('rd')
LIST_STOPWORDS_PORTUGUESE = stopwords.words('portuguese')
LIST_STOPWORDS_SPANISH = stopwords.words('spanish')
LIST_STOPWORDS_GERMAN = stopwords.words('german')
LIST_STOPWORDS_GERMAN.append('and')

# Exception List
EXCEPTION_LIST = ['arXiv', '-', '\&', '&']

#Create directories
path_current = os.getcwd() # Current directory
path_bib_original = os.path.join(path_current, "OriginalBIB")
path_reports = os.path.join(path_current, "GenerateReports")
path_bib = os.path.join(path_current, "GenerateBIB")

## Load configuration
def main():

    LANGUAGES = {
    "en": "english",
    "pt": "portuguese",
    }

    TYPES = {
        "num": "num-alpha",
        "alpha": "num-alpha",
        "apa": "apa",
    }

    #arguments entered via the command line
    argparser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    argparser.add_argument(dest="filename")
    argparser.add_argument(
        "-L",
        "--language",
        choices=LANGUAGES.keys(),
        help="Select a language { 'en' or 'pt' }",
        default="english",
    )
    argparser.add_argument(
        "-T",
        "--type",
        choices=TYPES.keys(),
        help="Select a type { 'num', 'alpha' or 'apa' }",
        default="num",
    )

    #for test
    '''
    LANGUAGE = 'en'
    print('LANGUAGE: ', LANGUAGE)
    LANGUAGE = LANGUAGES[LANGUAGE]

    TYPE_REFERENCES = 'num'
    print('TYPE_REFERENCES: ', TYPE_REFERENCES)
    TYPE_REFERENCES = TYPES[TYPE_REFERENCES]

    FILE_NAME = 'referencesTest.bib'
    print('FILE_NAME: ', FILE_NAME)
    '''
    #production
    #'''
    args = argparser.parse_args()
    LANGUAGE = args.language
    print('LANGUAGE: ', LANGUAGE)
    LANGUAGE = LANGUAGES[LANGUAGE]

    TYPE_REFERENCES = args.type
    print('TYPE_REFERENCES: ', TYPE_REFERENCES)
    TYPE_REFERENCES = TYPES[TYPE_REFERENCES]

    FILE_NAME = args.filename
    print('FILE_NAME: ', FILE_NAME)
    #'''
    NAME_FILE_OUTPUT_REPORT_MD = FILE_NAME[:-4] +"_Report_" + label_date + ".md"
    NAME_FILE_OUTPUT_REPORT_HTML = FILE_NAME[:-4] +"_Report_" + label_date + ".html"
    NAME_FILE_OUTPUT_BIB = FILE_NAME[:-4] + "_" + label_date + ".bib"

    file = open("results_temp.txt","w+",encoding="utf-8")

    lineHeader1 = "# References Report: " + str(label_date) + '\r'
    lineHeader2 = "## - Configurations: _Bib File:_ **"+ FILE_NAME +"** / _Language:_ **"+ LANGUAGE +"** / _Type References:_ **"+ TYPE_REFERENCES +"**\r\n"
    file.write(lineHeader1)
    file.write(lineHeader2)

    # ===========================================================
    # If repeated bibliograhpy entry or others erros
    msg_erros = ''
    stop = True
    read_error_bib = False
    error_command_line = False
    file_found = False
    #pass_language = False

    count = 0
    while stop == True:
        try:
            '''
            assert LANGUAGE in ['english', 'portuguese']
            pass_language = True
            assert TYPE_REFERENCES in ['apa', 'num-alpha']
            '''

            if os.path.exists("refer_find_errors_generate_temp.bib") == False:
                with os.scandir(path_bib_original) as entries:
                    for entry in entries:
                        if entry.name == FILE_NAME:
                            shutil.copyfile(os.path.join(path_bib_original, FILE_NAME), 'refer_find_errors_generate_temp.bib')
                            file_found = True
                            break

            if file_found == True:
                bib_data = parse_file('refer_find_errors_generate_temp.bib')
            else:
                error_command_line = True
                msg_erros += '- ## The name of the .bib file set as a parameter on the command line was not found in the bib file folder. '
                msg_erros += 'Check if it is actually in the folder (OriginalBIB) or if the file name was spelled correctly in the parameter.\r'

            stop = False
        except FileNotFoundError as identifier:
            error_command_line = True
            msg_erros += '- ## The name of the .bib file set as a parameter on the command line was not found in the bib file folder. '
            msg_erros += 'Check if it is actually in the folder (OriginalBIB) or if the file name was spelled correctly in the parameter.\r'
            stop = False
            '''
            except AssertionError as identifier:
                error_command_line = True

                if pass_language == True:
                    msg_erros += '- ## The value defined in the parameter of your reference type is not valid. '
                    msg_erros += 'Valid values: [`num`, `alpha` or `apa`].\r'
                else:
                    msg_erros += '- ## The value defined in your reference language parameter is not valid. '
                    msg_erros += 'Valid values: [`en` or `pt`].\r'

                stop = False
            '''
        except BibliographyDataError as identifier:
            read_error_bib = True

            count+=1
            msg_erros += '- ## ' + str(identifier) + '\r'
            tag_rep = str(identifier).split(':')

            #input file
            fin = open("refer_find_errors_generate_temp.bib", "rt",encoding="utf-8")
            contents = fin.read().replace(str(tag_rep[1]).strip(), str(tag_rep[1]).strip()+str(count), count)
            fin.close()

            fin = open("refer_find_errors_generate_temp.bib", "w+",encoding="utf-8")
            fin.write(contents)
            fin.close()

        except UndefinedMacro as identifier:
            read_error_bib = True
            erro = identifier.args[0]
            msg_erros += '- ## ' + str(identifier) + '\r'

            #input file
            fin = open("refer_find_errors_generate_temp.bib", "rt",encoding="utf-8")
            contents = fin.read().replace(erro, 'JAN')
            fin.close()

            fin = open("refer_find_errors_generate_temp.bib", "w+",encoding="utf-8")
            fin.write(contents)
            fin.close()

        except TokenRequired as identifier:
            read_error_bib = True
            erro = identifier.args[0]
            value_new = ''

            msg_erros += '## - ' + str(identifier) + '\r'

            #input file
            fin = open("refer_find_errors_generate_temp.bib", "rt",encoding="utf-8")
            contents = fin.read().replace(erro, value_new)
            fin.close()

            fin = open("refer_find_errors_generate_temp.bib", "w+",encoding="utf-8")
            fin.write(contents)
            fin.close()
            stop = False

    if os.path.exists("refer_find_errors_generate_temp.bib"):
        os.remove("refer_find_errors_generate_temp.bib")

    # ===========================================================

    if read_error_bib == True:
        line = '# Error reading your .bib file!\r\n'
        line += '### Errors may be related:\r'
        line += '- the label of repeated references. Repeated entries will be listed below. '
        line += 'Check the labels (tags) used before continuing to run the report.\r'
        line += '- information for month={WRONG}. This field must always be filled in English (even if its volume is in Portuguese), '
        line += 'nor can it be empty. '
        line += '(_Accepted formats: [Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec]_)\r\n'
        line += '## Errors found:\r'

        line_footer = '#### *Warning:* Correct repeated entries or month information in your original .bib file. '
        line_footer += '#### Afterwards, run this script again to generate the error report. \r'
        file.write(line)
        file.write(msg_erros+'\r\n')
        file.write(line_footer)

    elif error_command_line == True:
        line = '# Error trying to run your command line.!\r\n'
        line += '## Errors found:\r'

        line_footer = '#### Afterwards, run this script again to generate the error report. \r'
        file.write(line)
        file.write(msg_erros+'\r\n')
        file.write(line_footer)

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

        assert TYPE_REFERENCES in ['apa', 'num', 'alpha', 'num-alpha']
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

        bib_data = parse_file(os.path.join(path_bib_original, FILE_NAME))
        ##

        line1 = '| Error | Type |Tag | Title | Warning |' + '\r'
        line2 = '|-:|:---:|:---:|:---:|:------:|' + '\r'
        file.write(line1)
        file.write(line2)

        congratulations = False
        count=0
        tag_inv_global = False
        for entry in bib_data.entries:
            bib = bib_data.entries[entry]
            #print('entry: ============ ', entry)
            msg, tag_inv = check(bib, REQ, MONTHS, TYPE_REFERENCES)

            if tag_inv == False:
                msg_gen, bib = regenerate_bib(bib, REQ)
                msg+=msg_gen

                bib_data.entries[entry] = bib
            else:
                tag_inv_global = True

            if len(msg) > 0:
                count+=1
                line = '| ' + str(count) +' |@'+ bib.type + '| {' + str(entry) + '} |' + str(bib.fields['title']) + ' | ' + msg + ' | ' + '\r'
                file.write(line)


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
            congratulations = True
            lineCongrat1 = '# Congratulations! \r\n'
            lineCongrat2 = '## - No errors were identified in the fields. However, it is still necessary to check the standardization of your references, which this script does not guarantee.'
            file.write(lineCongrat1)
            file.write(lineCongrat2)

        if tag_inv_global == False and congratulations == False:

            file_bib = open(os.path.join(path_bib, NAME_FILE_OUTPUT_BIB),"w+", encoding="utf-8")

            file_bib.write(bib_data.to_string('bibtex'))
            file_bib.close()

            if LANGUAGE == 'portuguese':
                fin = open(os.path.join(path_bib, NAME_FILE_OUTPUT_BIB), "rt+",encoding="utf-8")
                contents = ''
                for index, month in enumerate(MONTHS_ENG_VALID):
                    month_pt = MONTHS_PORT_VALID[index].upper()
                    contents += fin.read().replace(month, month_pt)

                fin.close()

                fin = open(os.path.join(path_bib, NAME_FILE_OUTPUT_BIB), "w+",encoding="utf-8")
                fin.write(contents)
                fin.close()

    file.close()

    shutil.copyfile("results_temp.txt", NAME_FILE_OUTPUT_REPORT_MD)

    command = "grip "+NAME_FILE_OUTPUT_REPORT_MD+" --export "+NAME_FILE_OUTPUT_REPORT_HTML
    os.system(command)

    del_html = False
    if os.path.exists(NAME_FILE_OUTPUT_REPORT_HTML):
        file_html = open(NAME_FILE_OUTPUT_REPORT_HTML, "rt",encoding="utf-8")
        contents = file_html.read()

        if '500 Internal Server Error' in contents:
            del_html = True
        file_html.flush()
        file_html.close()

    else:
        del_html = True

    if del_html == True:
        shutil.copyfile(NAME_FILE_OUTPUT_REPORT_MD, os.path.join(path_reports, NAME_FILE_OUTPUT_REPORT_MD))
    else:
        shutil.copyfile(NAME_FILE_OUTPUT_REPORT_HTML, os.path.join(path_reports, NAME_FILE_OUTPUT_REPORT_HTML))

    if os.path.exists("results_temp.txt"):
        os.remove("results_temp.txt")
    if os.path.exists(NAME_FILE_OUTPUT_REPORT_MD):
        os.remove(NAME_FILE_OUTPUT_REPORT_MD)
    if os.path.exists(NAME_FILE_OUTPUT_REPORT_HTML):
        os.remove(NAME_FILE_OUTPUT_REPORT_HTML)


def regenerate_bib(bib, REQ):
    list_fields_keys = [field_key.lower() for field_key in bib.fields.keys()]
    list_fields_persons = [field_person.lower() for field_person in bib.persons.keys()]
    fields = set(list_fields_keys + list_fields_persons)
    missing = REQ[bib.type].difference(fields)

    msg = ''

    if bib.type == 'book' or bib.type == 'inbook':
        exist = 'publisher' in missing
        if exist == False:
            phrase = bib.fields['publisher']
            msg_year, phrase = find_year(phrase, 'publisher')
            msg += msg_year

            publisher_capitalize, phrase_cap = check_parentheses_and_capitalize(phrase)

            #capitalize
            if len(phrase_cap) > 0:
                bib.fields['publisher'] = phrase_cap

            if publisher_capitalize == True:
                msg += 'Field { publisher } is not capitalized; '

    if bib.type == 'article':
        exist = 'journal' in missing
        if exist == False:
            phrase = bib.fields['journal']
            msg_year, phrase = find_year(phrase, 'journal')
            msg += msg_year

            journal_capitalize, phrase_cap = check_parentheses_and_capitalize(phrase)

            #capitalize
            if len(phrase_cap) > 0:
                bib.fields['journal'] = phrase_cap

            if journal_capitalize == True:
                msg += 'Field { journal } is not capitalized; '

    if bib.type == 'inproceedings' or bib.type == 'proceedings' or bib.type == 'incollection' or bib.type == 'conference':
        exist = 'booktitle' in missing
        if exist == False:
            phrase = bib.fields['booktitle']
            msg_year, phrase = find_year(phrase, 'booktitle')
            msg += msg_year

            booktitle_capitalize, phrase_cap = check_parentheses_and_capitalize(phrase)

            #capitalize
            if len(phrase_cap) > 0:
                bib.fields['booktitle'] = phrase_cap

            if booktitle_capitalize == True:
                msg += 'Field { booktitle } is not capitalized; '

    if bib.type == 'mastherthesis' or bib.type == 'phdthesis':
        exist = 'school' in missing
        if exist == False:
            phrase = bib.fields['school']
            msg_year, phrase = find_year(phrase, 'school')
            msg += msg_year

            school_capitalize, phrase_cap = check_parentheses_and_capitalize(phrase)

            #capitalize
            if len(phrase_cap) > 0:
                bib.fields['school'] = phrase_cap

            if school_capitalize == True:
                msg += 'Field { school } is not capitalized; '

    if bib.type == 'techreport':
        exist = 'institution' in missing
        if exist == False:
            phrase = bib.fields['institution']
            msg_year, phrase = find_year(phrase, 'institution')
            msg += msg_year

            institution_capitalize, phrase_cap = check_parentheses_and_capitalize(phrase)

            #capitalize
            if len(phrase_cap) > 0:
                bib.fields['institution'] = phrase_cap

            if institution_capitalize == True:
                msg += 'Field { institution } is not capitalized; '

    if bib.type in REQ.keys():
        for value in missing:
            bib.fields[value] = 'MISSING'

    return msg, bib

##
def check(bib, req, months, type_references):
    list_fields_keys = [field_key.lower() for field_key in bib.fields.keys()]
    list_fields_persons = [field_person.lower() for field_person in bib.persons.keys()]
    fields = set(list_fields_keys + list_fields_persons)

    msg = ''
    tag_inv = False
    if bib.type not in req.keys():
        msg = 'Type not implemented: [@' + bib.type + '] remove or replace; '
        tag_inv = True
    else:
        if type_references == 'apa':
            if bib.type == 'article' and 'year' in fields:
                year_month_check = check_article_year_month(bib.fields['year'], months, type_references)
                if not year_month_check:
                    msg += 'Failed Month and Year: year={Mon, Year} check; '
        if type_references == 'num-alpha':
            if bib.type == 'article' and 'month' in fields:
                month_check = check_article_year_month(bib.fields['month'], months, type_references)
                if not month_check:
                    msg += 'Failed Month month={ Mon } check; '

        missing = req[bib.type].difference(fields)
        if len(missing) > 0:
            msg += 'Missing: ' + str(missing) + "; "

    return msg, tag_inv

def find_year(phrase, tag):
    msg = ''
    result = re.findall(re.compile('.*([1-3][0-9]{3})'), phrase)
    if len(result) > 0:
        msg = 'The {'+tag+'} field takes no year information:  '+ str(result) +' remove; '
        phrase = phrase.replace(str(result[0]), '')

    return msg, phrase

def check_parentheses_and_capitalize(phrase):
    language = detect(phrase)

    #remove parenthesis
    phrase = re.sub(r"\((.*?)\)", ' ', phrase)

    words = phrase.split()
    words_aux = []

    uncapitalized = False
    hif = False
    word2 = ''
    STOP_LIST = []
    if language == 'en':
        STOP_LIST = LIST_STOPWORDS_ENGLISH
    elif language == 'pt':
        STOP_LIST = LIST_STOPWORDS_PORTUGUESE
    elif language == 'es':
        STOP_LIST = LIST_STOPWORDS_SPANISH
    elif language == 'de':
        STOP_LIST = LIST_STOPWORDS_GERMAN
    else:
        STOP_LIST = LIST_STOPWORDS_ENGLISH

    for word in words:
        if word not in STOP_LIST:
            if "-" in word and word != '-':
                hif = True
                words_hifen = word.split('-')
                word = words_hifen[0]
                word2 = words_hifen[1]
            if word == 'e': # e-Business, e-Science, ...
                 words_aux.append(word+"-"+word2)
            elif word in EXCEPTION_LIST:
                words_aux.append(word)
            elif word[0].isdigit() == True:
                words_aux.append(word)
            else:
                if word.isupper() == False:
                    if word[0].isupper() == False:
                    #if word != word.capitalize():
                        uncapitalized = True
                        if hif == True:
                            words_aux.append(word.capitalize()+"-"+word2)
                        else:
                            words_aux.append(word.capitalize())
                    else:
                        if hif == True:
                            words_aux.append(word+"-"+word2)
                        else:
                            words_aux.append(word)
                else:
                    words_aux.append("{"+word+"}")
        else:
            words_aux.append(word)


    if uncapitalized == True:
        phrase_cap = ' '.join([word for word in words_aux])
    else:
        phrase_cap = ''

    return uncapitalized, phrase_cap

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
