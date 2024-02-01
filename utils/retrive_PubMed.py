



####################################################  HOW TO USE #######################################
# import sys
# import os
# module_path = os.path.abspath(os.path.join('..'))
# if module_path not in sys.path:
#     sys.path.append(module_path+"//utils")
# import retrive_PubMed

# import importlib
# importlib.reload(retrive_PubMed)



# Solution two:

# Step 1: Create setup.py 

# from setuptools import setup, find_packages  
# setup(name = 'utils', packages = find_packages())

# Step 2: Running setup.py file 

# python setup.py install


####################################################  HOW TO USE #######################################



# #Extract artcile titles which contain specific terms
from attr import field
from nltk.corpus import stopwords
import nltk

stop_words = set(stopwords.words('english'))

from nltk.tokenize import word_tokenize    
import string



sentence_tokenizer=nltk.data.load('tokenizers/punkt/english.pickle')

# from Bio import Entrez
# import requests
# import json

# def pre_process(LSF_term):

#     """ remove Punctutations and stop wrods and return the list of splitted key-words in the LSF-term"""
#     stop_words = set(stopwords.words('english'))

#     translator = str.maketrans(string.punctuation, ' '*len(string.punctuation)) #map punctuation to space
#     LSF_term=LSF_term.translate(translator)
#     word_tokens = word_tokenize(LSF_term) 
#     filtered_LSF_Term = [w for w in word_tokens if not w.lower() in stop_words]
    
#     return filtered_LSF_Term




#! pip install biopython

from Bio import Entrez


Entrez.email = 'esmaeil.nourani@gmail.com'
Entrez.api_key=''  # api_key Personal API key from NCBI. If not set, only 3 queries per second are allowed. 10 queries per seconds otherwise with a valid API key.


def pre_process(LSF_term):

    """ remove Punctutations and stop wrods and return the list of splitted key-words in the LSF-term"""

    translator = str.maketrans(string.punctuation, ' '*len(string.punctuation)) #map punctuation to space
    LSF_term=LSF_term.translate(translator)
    word_tokens = word_tokenize(LSF_term) 
    filtered_LSF_Term = [w for w in word_tokens if not w.lower() in stop_words]
    
    return ' '.join(filtered_LSF_Term)
    




# def get_pmids_old(LSF_term):

#     """ Extract pmids which contain the interested LSF term in the title"""
#     pmid_list=None
#     db = 'pubmed'
#     domain = 'https://www.ncbi.nlm.nih.gov/entrez/eutils'
#     nresults = 100  # retuens 100 artcil titles
#     field='title' # search within artcile titles
#     retmode='json'
#     # standard query
#     LSF_term=pre_process(LSF_term)  # remove punctuation and stopwords
#     queryLinkSearch = f'{domain}/esearch.fcgi?db={db}&retmax={nresults}&retmode={retmode}&term={LSF_term}&field={field}'
#     response = requests.get(queryLinkSearch)
#     try:
#         pubmedJson = response.json()
#         pmid_list=pubmedJson["esearchresult"]["idlist"]
#         pmid_list=[int(pmid) for pmid in pmid_list ]
#     except:
#         pass
    
#     return pmid_list



from tqdm import tqdm






def get_pmids(LSF_term,count=100,field='title'):
    """Retrieves pubmedis which contain the 'LSF_term' in their titles

    Args:
        LSF_term (str): query keyword
        count: number of PubmedIds to be returned
        field: Search field. If used, the entire search term will be limited to the specified Entrez field, Default(Title), search only in the article Titles
    Returns:
        pmid_list
        total_hit_count: 
    """

    processed_name=LSF_term.replace(' ','+')
    Entrez.email = 'esmaeil.nourani@gmail.com'
    Entrez.api_key=''  # api_key Personal API key from NCBI. If not set, only 3 queries per second are allowed. 10 queries per seconds otherwise with a valid API key.

    handle = Entrez.esearch(db="pubmed", retmax=count, term=processed_name,field=field,sort='Relevance')  # search within artcile titles and return at most 100 artcil titles
    record = Entrez.read(handle)   
    handle.close()

    pmid_list=record['IdList']
    total_hit_count=record['Count']  

    return pmid_list,total_hit_count






def get_title(LSF_term,count=100,field='title'):
    """Retrieves 100 titles for a single LSF term

    Args:
        LSF_term (str): query keyword
        count: number of PubmedIds to be returned
        field: Search field. If used, the entire search term will be limited to the specified Entrez field, Default(Title), search only in the article Titles

    Returns:
        titles:  list of article titles
    """
    
   
    Entrez.email = 'esmaeil.nourani@gmail.com'
    Entrez.api_key=''  # api_key Personal API key from NCBI. If not set, only 3 queries per second are allowed. 10 queries per seconds otherwise with a valid API key.

    pmid_list,total_hit_count=get_pmids(LSF_term,count=count,field=field)



    if int(total_hit_count)==0:
        return [],0      # the result set is empty

    handle = Entrez.efetch(db="pubmed", id=','.join(map(str, pmid_list)),
                           rettype="xml", retmode="text")
    records = Entrez.read(handle)


    # The following part can be replaced by titles if we want to extract the whole abstract

    #     abstracts = [pubmed_article['MedlineCitation']['Article']['Abstract'] ['AbstractText'][0] 
    #              for pubmed_article in records['PubmedArticle'] if 'Abstract' in
    #              pubmed_article['MedlineCitation']['Article'].keys()]

    
    
    
    titles = [pubmed_article['MedlineCitation']['Article']['ArticleTitle']
                  for pubmed_article in records['PubmedArticle']]
    
    return titles,int(total_hit_count)














def get_docs(LSF_terms,count=100,field='title',returned_field='title'):
    """Retrieve 100 titles per each requested LSF term 

    Args:
        LSF_term (str): list of query keywords
        count: number of PubmedIds to be returned
        field: Search field. If used, the entire search term will be limited to the specified Entrez field, Default(Title), search only in the article Titles- Other option: 'abstract'
        returned_field: which part of the paper should be returned as the requested context==> title or abstract
        

    Returns:
        docs:  list of article titles, each entry is a concatination of 100 titles
        not_matched_indices
    """
    

    Entrez.email = 'esmaeil.nourani@gmail.com'
    Entrez.api_key=''  # api_key Personal API key from NCBI. If not set, only 3 queries per second are allowed. 10 queries per seconds otherwise with a valid API key.


    docs=[]
    #not_matched_indices=[]
    hit_counts=[]
    for i,name in tqdm(enumerate(LSF_terms)):
        try:
            handle = Entrez.esearch(db="pubmed", retmax=count, term=name,field=field,sort='Relevance')  # search within artcile titles and return at most 100 artcil titles
        except:
            continue

        record = Entrez.read(handle)   
        #handle.close()
        pmid_list=record['IdList']
        total_hit_count=int(record['Count'])  

        if total_hit_count==0:
            hit_counts.append(total_hit_count)
            docs.append(name)
            continue
        try:
            handle = Entrez.efetch(db="pubmed", id=','.join(map(str, pmid_list)),rettype="xml", retmode="text")
        except:
            continue

        records = Entrez.read(handle)



        if  returned_field=='title':   # contexts are gathered from artcile titles

            
            contexts = [pubmed_article['MedlineCitation']['Article']['ArticleTitle']
                        for pubmed_article in records['PubmedArticle']]
        

        elif returned_field=='abstract':   # contexts are gathered from artcile abstracts

            contexts = [pubmed_article['MedlineCitation']['Article']['Abstract'] ['AbstractText'][0] 
                    for pubmed_article in records['PubmedArticle'] if 'Abstract' in
                    pubmed_article['MedlineCitation']['Article'].keys()]




        doc_candidate=' '.join(contexts)
        hit_counts.append(total_hit_count)
        docs.append(doc_candidate)

    return docs,hit_counts







# This version also return the actual returned count
def get_docs_new(LSF_terms,count=100,field='title',returned_field='title'):
    """Retrieve 100 titles per each requested LSF term 

    Args:
        LSF_term (str): list of query keywords
        count: number of PubmedIds to be returned
        field: Search field. If used, the entire search term will be limited to the specified Entrez field, Default(Title), search only in the article Titles- Other option: 'abstract'
        returned_field: which part of the paper should be returned as the requested context==> title or abstract
        

    Returns:
        docs:  list of article titles, each entry is a concatination of 100 titles
        not_matched_indices
         hit_counts : number is returned as hit count from entrez 
         returned_counts: actual hit count which is used to produce context
    """
    

    Entrez.email = 'esmaeil.nourani@gmail.com'
    Entrez.api_key=''  # api_key Personal API key from NCBI. If not set, only 3 queries per second are allowed. 10 queries per seconds otherwise with a valid API key.


    docs=[]
    #not_matched_indices=[]
    hit_counts=[]
    returned_counts=[]
    for i,name in tqdm(enumerate(LSF_terms)):

        handle = Entrez.esearch(db="pubmed", retmax=count, term=name,field=field,sort='Relevance')  # search within artcile titles and return at most 100 artcil titles
        record = Entrez.read(handle)   
        #handle.close()
        pmid_list=record['IdList']
        total_hit_count=int(record['Count'])  

        if total_hit_count==0:
            hit_counts.append(total_hit_count)
            docs.append(name)
            continue

        handle = Entrez.efetch(db="pubmed", id=','.join(map(str, pmid_list)),
                            rettype="xml", retmode="text")
        records = Entrez.read(handle)



        if  returned_field=='title':   # contexts are gathered from artcile titles

            
            contexts = [pubmed_article['MedlineCitation']['Article']['ArticleTitle']
                        for pubmed_article in records['PubmedArticle']]
        

        elif returned_field=='abstract':   # contexts are gathered from artcile abstracts

            contexts = [pubmed_article['MedlineCitation']['Article']['Abstract'] ['AbstractText'][0] 
                    for pubmed_article in records['PubmedArticle'] if 'Abstract' in
                    pubmed_article['MedlineCitation']['Article'].keys()]


        returned_count=len(contexts)
        returned_counts.append(returned_count)


        doc_candidate=' '.join(contexts)
        hit_counts.append(total_hit_count)
        docs.append(doc_candidate)

    return docs,hit_counts,returned_counts



import re

#from .utils_general import term_in_sentence
from utils_general import term_in_sentence

def get_sentences(LSF_terms,count):
    """Retrieve 100 articles per each requested LSF term 
        if requested number of sentences can be found in th article titles they will be conctanetaed and will be returned as the context
        otherwise
        accumulated context from context(which is not still enough) will be combined by the sentences from abstract which contain the target term

    Args:
        LSF_term (str): list of query keywords
        count: number of PubmedIds to be returned
       

    Returns:
        docs:  list of concatenated sentences, each entry is for single LSF term 
        not_matched_indices
         hit_counts : number is returned as hit count from entrez 
         returned_counts: actual sentence count which is used to produce context for the target LSF term
    """
    
    sentence_tokenizer=nltk.data.load('tokenizers/punkt/english.pickle')

    Entrez.email = 'esmaeil.nourani@gmail.com'
    Entrez.api_key=''  # api_key Personal API key from NCBI. If not set, only 3 queries per second are allowed. 10 queries per seconds otherwise with a valid API key.


    docs=[]
    #not_matched_indices=[]
    hit_counts=[]
    returned_counts=[]
    for i,name in tqdm(enumerate(LSF_terms)):

        processed_name=name.replace(' ','+')
        try:
            context_from_titles,title_hit_count=get_title(processed_name,count)
        except:
            hit_counts.append(0)
            docs.append(name) 
            returned_counts.append(0)
            continue

        if len(context_from_titles) >= count:    #only titles are enough to generate context so ignore the rest for the current name and jump to the next name
            hit_counts.append(title_hit_count)
            docs.append(' '.join(context_from_titles)) 
            returned_counts.append(count)
            continue


        # if titles are not enough continue to add some sentences from abstracts
        #print('titles not enough: ', len(context_from_titles))
        try:
            handle = Entrez.esearch(db="pubmed", retmax=100, term=processed_name,sort='Relevance') 
        except:
            hit_counts.append(0)
            docs.append(name) 
            returned_counts.append(0)
            continue
        record = Entrez.read(handle)   
        #handle.close
        pmid_list=record['IdList']
        total_hit_count=int(record['Count'])

        if total_hit_count==0:    # there is no enough context for the current name, continue to the next
            #print('hit count is not enough ', total_hit_count )
            hit_counts.append(total_hit_count)
            docs.append(name) # append name it self instead of any context
            returned_counts.append(0)
            continue
        try:
            handle = Entrez.efetch(db="pubmed", id=','.join(map(str, pmid_list)),rettype="xml", retmode="text")
        except:
            hit_counts.append(0)
            docs.append(name) 
            returned_counts.append(0)
            continue

        records = Entrez.read(handle)



        contexts = [pubmed_article['MedlineCitation']['Article']['Abstract'] ['AbstractText'][0] 
                for pubmed_article in records['PubmedArticle'] if 'Abstract' in
                pubmed_article['MedlineCitation']['Article'].keys()]


        # Merge the abstracts
        doc_candidate=' '.join(contexts)


        # Split abstracts to sentences
        sentence_list = sentence_tokenizer.tokenize(doc_candidate)
        
        # Select sentences which contain the target name
        context=' '.join(context_from_titles)
        returned_count=len(context_from_titles)
        for sent in sentence_list:

            if term_in_sentence(name,sent):
                 returned_count+=1
                 context+=sent
                 if returned_count==count:
                    break

            # try:
            #     if re.search(r"\b{}\b".format(name.lower()), sent.lower().strip()):   # name exist in the sentence
            #         returned_count+=1
            #         context+=sent
            #         if returned_count==count:
            #             break
            # except:
            #     continue

        docs.append(context)
        hit_counts.append(total_hit_count)
        returned_counts.append(returned_count) # Number of sentences are concatenated to be returned as the context


    return docs,hit_counts,returned_counts









def get_match_counts(LSF_terms):
    """ qury the match count for list names from PubMed

    Args:
        LSF_terms (list): list of names to be quieried from PubMed
    """
 
    Entrez.email = 'esmaeil.nourani@gmail.com'
    Entrez.api_key=''  # api_key Personal API key from NCBI. If not set, only 3 queries per second are allowed. 10 queries per seconds otherwise with a valid API key.

    match_counts=[]
    for i,name in tqdm(enumerate(LSF_terms)):

        processed_name=name.replace(' ','+')

        #processed_name='"'+processed_name+'" disease' 
        #processed_name='"'+processed_name+'"' +"AND+%28health+OR+disease%29"
        processed_name='"'+processed_name+'"' +" AND + ( health OR disease)"
        
        


        try:
            handle = Entrez.esearch(db="pubmed", retmax=1, term=processed_name,sort='Relevance') 
        except:
            match_counts.append(0)
            continue
        record = Entrez.read(handle)   
        
        total_match_count=int(record['Count'])
        
        match_counts.append(total_match_count)
    return match_counts












#from .utils_general import term_in_sentence
from utils_general import term_in_sentence

def get_sentences_separated(LSF_terms,count):
    """Retrieve 100 articles per each requested LSF term 
        if requested number of sentences can be found in th article titles they will be conctanetaed and will be returned as the context
        otherwise
        accumulated context from context(which is not still enough) will be combined by the sentences from abstract which contain the target term

    Args:
        LSF_term (str): list of query keywords
        count: number of PubmedIds to be returned
       

    Returns:
        docs:  list of concatenated sentences, each entry is for single LSF term 
        not_matched_indices
         hit_counts : hit count all
         hit_counts_title: hit count only in title
    """
    
    sentence_tokenizer=nltk.data.load('tokenizers/punkt/english.pickle')

    Entrez.email = 'esmaeil.nourani@gmail.com'
    Entrez.api_key=''  # api_key Personal API key from NCBI. If not set, only 3 queries per second are allowed. 10 queries per seconds otherwise with a valid API key.


    docs=[]
    #not_matched_indices=[]
    hit_counts=[]
    hit_counts_title=[]
    try:
        for i,name in tqdm(enumerate(LSF_terms)):

            processed_name=name.replace(' ','+')

            processed_name='"'+processed_name+'"'
            #processed_name='"'+name+'"'  # add quotationa marks 
            try:
                context_from_titles,title_hit_count=get_title(processed_name,count)
            except:
                context_from_titles=[]
                title_hit_count=0



            # if titles are not enough continue to add some sentences from abstracts
            try:
                handle = Entrez.esearch(db="pubmed", retmax=100, term=processed_name,sort='Relevance') 
            except:
                docs.append([name]) 
                hit_counts.append(0)
                hit_counts_title.append(title_hit_count)

                continue
            record = Entrez.read(handle)   
            pmid_list=record['IdList']
            total_hit_count=int(record['Count'])


            if len(context_from_titles) >= count  :    #only titles are enough to generate context so ignore the rest for the current name and jump to the next name
                docs.append(context_from_titles)    
                hit_counts.append(total_hit_count)
                hit_counts_title.append(title_hit_count)
                                    
                continue
            

            if total_hit_count==0:   
                if len( context_from_titles )==0:
                    docs.append([name]) # append name it self instead of any context
                else:
                    docs.append(context_from_titles)  # there is content for title
                hit_counts.append(total_hit_count)
                hit_counts_title.append(title_hit_count)
                continue  # there is no enough context for the current name, continue to the next

            try:
                handle = Entrez.efetch(db="pubmed", id=','.join(map(str, pmid_list)),rettype="xml", retmode="text")
            except:
                if len( context_from_titles )==0:
                    docs.append([name]) # append name it self instead of any context
                else:
                    docs.append(context_from_titles)  # there is content for title
                
                hit_counts.append(total_hit_count)
                hit_counts_title.append(title_hit_count)
                continue  # there is no enough context for the current name, continue to the next

            records = Entrez.read(handle)



            contexts = [pubmed_article['MedlineCitation']['Article']['Abstract'] ['AbstractText'][0] 
                    for pubmed_article in records['PubmedArticle'] if 'Abstract' in
                    pubmed_article['MedlineCitation']['Article'].keys()]


            # Merge the abstracts
            doc_candidate=' '.join(contexts)


            # Split abstracts to sentences
            sentence_list = sentence_tokenizer.tokenize(doc_candidate)
            
            # Select sentences which contain the target name
            #context=' '.join(context_from_titles)
            context=context_from_titles
            for sent in sentence_list:

                #if term_in_sentence(name,sent):
                if name.lower() in sent.lower():
                    #context+=sent
                    context.append(sent)
                    if len(context)>=count:
                        break

                # try:
                #     if re.search(r"\b{}\b".format(name.lower()), sent.lower().strip()):   # name exist in the sentence
                #         returned_count+=1
                #         context+=sent
                #         if returned_count==count:
                #             break
                # except:
                #     continue

            docs.append(context)
            hit_counts.append(total_hit_count)
            hit_counts_title.append(title_hit_count)

    except Exception as e:
            return docs,hit_counts,hit_counts_title, str(e)


    return docs,hit_counts,hit_counts_title,'done without error'








def get_abstract_sentences_candidates(df_candidates,count):
    """Retrieve 100 articles per each requested LSF term 
        if requested number of sentences can be found in th article titles they will be conctanetaed and will be returned as the context
        otherwise
        accumulated context from context(which is not still enough) will be combined by the sentences from abstract which contain the target term

    Args:
        LSF_term (str): list of query keywords
        count: number of PubmedIds to be returned
       

    Returns:
        docs:  list of concatenated sentences, each entry is for single LSF term 
        not_matched_indices
         hit_counts : number is returned as hit count from entrez 
         returned_counts: actual sentence count which is used to produce context for the target LSF term
    """
    
    sentence_tokenizer=nltk.data.load('tokenizers/punkt/english.pickle')

    Entrez.email = 'esmaeil.nourani@gmail.com'
    Entrez.api_key=''  # api_key Personal API key from NCBI. If not set, only 3 queries per second are allowed. 10 queries per seconds otherwise with a valid API key.


    docs=[]
    #not_matched_indices=[]
    hit_counts=[]
    returned_counts=[]
    for i,row in tqdm((df_candidates.iterrows())):
        name=row['related_name']
        processed_name=name.replace(' ','+')
        try:
            context_from_titles,title_hit_count=get_title(processed_name,count)
        except:
            hit_counts.append(0)
            docs.append(name) 
            returned_counts.append(0)
            continue

        if len(context_from_titles) >= count:    #only titles are enough to generate context so ignore the rest for the current name and jump to the next name
            hit_counts.append(title_hit_count)
            docs.append(' '.join(context_from_titles)) 
            returned_counts.append(count)
            continue


        # if titles are not enough continue to add some sentences from abstracts
        #print('titles not enough: ', len(context_from_titles))
        try:
            handle = Entrez.esearch(db="pubmed", retmax=100, term=processed_name,sort='Relevance') 
        except:
            hit_counts.append(title_hit_count)
            docs.append(' '.join(context_from_titles)) 
            returned_counts.append(count)
            continue
        record = Entrez.read(handle)   
        #handle.close
        pmid_list=record['IdList']
        total_hit_count=int(record['Count'])

        if total_hit_count==0:    # there is no enough context for the current name, continue to the next
            #print('hit count is not enough ', total_hit_count )
            hit_counts.append(total_hit_count)
            docs.append(name) # append name it self instead of any context
            returned_counts.append(0)
            continue
        try:
            handle = Entrez.efetch(db="pubmed", id=','.join(map(str, pmid_list)),rettype="xml", retmode="text")
        except:
            continue

        records = Entrez.read(handle)



        contexts = [pubmed_article['MedlineCitation']['Article']['Abstract'] ['AbstractText'][0] 
                for pubmed_article in records['PubmedArticle'] if 'Abstract' in
                pubmed_article['MedlineCitation']['Article'].keys()]


        # Merge the abstracts
        doc_candidate=' '.join(contexts)


        # Split abstracts to sentences
        sentence_list = sentence_tokenizer.tokenize(doc_candidate)
        
        # Select sentences which contain the target name
        context=' '.join(context_from_titles)
        returned_count=len(context_from_titles)
        for sent in sentence_list:

            if term_in_sentence(name,sent):
                 returned_count+=1
                 context+=sent
                 if returned_count==count:
                    break

            # try:
            #     if re.search(r"\b{}\b".format(name.lower()), sent.lower().strip()):   # name exist in the sentence
            #         returned_count+=1
            #         context+=sent
            #         if returned_count==count:
            #             break
            # except:
            #     continue

        docs.append(context)
        hit_counts.append(total_hit_count)
        returned_counts.append(returned_count) # Number of sentences are concatenated to be returned as the context

    df_candidates['context']=docs
    df_candidates['hit_counts']=hit_counts
    df_candidates['returned_counts']=returned_counts

    return df_candidates





def get_abstract_sentences(LSF_terms,count,min_hitCount=0,field='abstract'):
    """Retrieve 100 articles per each requested LSF term 
        Returned setences will be eculsively from abstracts and not titles
    Args:
        LSF_term (str): list of query keywords
        count: number of PubmedIds to be returned
        min_hitCount: minimum hit count to be considered
        field: search fro query term in title or abstract
       

    Returns:
        docs:  list of concatenated sentences, each entry is for single LSF term 
        not_matched_indices
         hit_counts : number is returned as hit count from entrez 
         returned_counts: actual sentence count which is used to produce context for the target LSF term
    """
   

    docs=[]
    #not_matched_indices=[]
    hit_counts=[]
    returned_counts=[]
    #for i,name in tqdm(enumerate(LSF_terms)):
    for i,name in enumerate(LSF_terms):
        name=str(name)
        processed_name=name.replace(' ','+')

        try:
            # Extract 3 times more abstracts, because all won't be matched
            handle = Entrez.esearch(db="pubmed", retmax=3*count, term=processed_name,field=field,sort='Relevance',spell=False) 
        except:
            hit_counts.append(0)
            docs.append(name) # append name it self instead of any context
            returned_counts.append(0)
            continue
        record = Entrez.read(handle)   
        #handle.close
        
        total_hit_count=int(record['Count'])
        
        if total_hit_count<=min_hitCount:    # there is no enough context for the current name, continue to the next
            #print('hit count is not enough ', total_hit_count )
            hit_counts.append(total_hit_count)
            docs.append(name) # append name it self instead of any context
            returned_counts.append(0)
            continue
        
        pmid_list=record['IdList']

        try:
            handle = Entrez.efetch(db="pubmed", id=','.join(map(str, pmid_list)),rettype="xml", retmode="text")
        except:
            hit_counts.append(0)
            docs.append(name) # append name it self instead of any context
            returned_counts.append(0)
            continue

        records = Entrez.read(handle)

        contexts = [pubmed_article['MedlineCitation']['Article']['Abstract'] ['AbstractText'][0] 
                for pubmed_article in records['PubmedArticle'] if 'Abstract' in
                pubmed_article['MedlineCitation']['Article'].keys()]


        # Merge the abstracts
        doc_candidate=' '.join(contexts)


        # Split abstracts to sentences
        sentence_list = sentence_tokenizer.tokenize(doc_candidate)
        # Select sentences which contain the target name
        context=''
        returned_count=0
        for sent in sentence_list:

            if term_in_sentence(name,sent):
                 returned_count+=1
                 context+=sent
                 if returned_count==count:
                    break

            # try:
            #     if re.search(r"\b{}\b".format(name.lower()), sent.lower().strip()):   # name exist in the sentence
            #         returned_count+=1
            #         context+=sent
            #         if returned_count==count:
            #             break
            # except:
            #     continue
        if context=='':
            docs.append(name)
        else:
            docs.append(context)
        hit_counts.append(total_hit_count)
        returned_counts.append(returned_count) # Number of sentences are concatenated to be returned as the context


    return docs,hit_counts,returned_counts






def get_abstract_by_pmid(pmid):
    """get_abstract_by_pmid

    Args:
        pmid (str): pmid
    """

  
    try:
        handle = Entrez.efetch(db="pubmed", id=pmid,rettype="xml", retmode="text")
    except:
        return ''

    records = Entrez.read(handle)

    contexts = [pubmed_article['MedlineCitation']['Article']['Abstract'] ['AbstractText'][0] 
            for pubmed_article in records['PubmedArticle'] if 'Abstract' in
            pubmed_article['MedlineCitation']['Article'].keys()]


    # Merge the abstracts
    return ' '.join(contexts)
