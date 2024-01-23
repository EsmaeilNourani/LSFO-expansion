import obonet
import networkx as nx
import copy
from collections import  defaultdict
import pandas as pd
def read_LSFC_new(LSFC_file):
    """ Produce id_to_name,name_to_id,id_to_synonyms,id_2_childs,id_2_parents

    Args:
        LSFC_file (str): path to LSFC

    Returns:
         id_to_name,name_to_id,id_to_synonyms,id_2_childs,id_2_parents
    """
    graph = obonet.read_obo(LSFC_file)
    id_to_name = {id_: data.get('name') for id_, data in graph.nodes(data=True)}
    name_to_id = {data['name']: id_ for id_, data in graph.nodes(data=True) if 'name' in data}
    # stores the synonyms of a name and dived them into "Exact" and "Related" synonyms
    id_to_synonyms=defaultdict(lambda: defaultdict(list))
    id_to_xrefs=defaultdict(lambda: defaultdict(list))
    categories=list(graph.predecessors('LFID:0000000'))
    id_2_childs=defaultdict(lambda: defaultdict(list))
    id_2_parents=defaultdict(lambda: defaultdict(list))

    id_to_xrefs=defaultdict(list)
    for id_, data in graph.nodes(data=True):
        if data.get('xref'):
            for xref in data.get('xref'):
                id_to_xrefs[id_].append(xref)

    for a,b,key in graph.in_edges(keys=True):
        id_2_childs[b][key].append(a)
        
    for a,b,key in graph.out_edges(keys=True):
        id_2_parents[a][key].append(b)

    for id_, data in graph.nodes(data=True):
        synonyms=data.get('synonym')
        categories=list(graph.predecessors('LFID:0000000'))        
        if synonyms:
            for syn in synonyms:

                if 'EXACT' in syn:

                    # Extract the name
                    id_to_synonyms[id_]['EXACT'].append(syn.split('"')[1])

                #elif 'RELATED' in syn:
                else:
                    # Extract the name
                    id_to_synonyms[id_]['RELATED'].append(syn.split('"')[1])
                
    return id_to_name,name_to_id,id_to_synonyms,id_2_childs,id_2_parents,id_to_xrefs

def read_LSFC(LSFC_file):
    """ Produce id_to_name,name_to_id,id_to_synonyms,id_2_childs,id_2_parents

    Args:
        LSFC_file (str): path to LSFC

    Returns:
         id_to_name,name_to_id,id_to_synonyms,id_2_childs,id_2_parents
    """
    graph = obonet.read_obo(LSFC_file)
    id_to_name = {id_: data.get('name') for id_, data in graph.nodes(data=True)}
    name_to_id = {data['name']: id_ for id_, data in graph.nodes(data=True) if 'name' in data}
    # stores the synonyms of a name and dived them into "Exact" and "Related" synonyms
    id_to_synonyms=defaultdict(lambda: defaultdict(list))
    id_to_xrefs=defaultdict(lambda: defaultdict(list))
    categories=list(graph.predecessors('LFID:0000000'))
    id_2_childs=defaultdict(lambda: defaultdict(list))
    id_2_parents=defaultdict(lambda: defaultdict(list))

    for a,b,key in graph.in_edges(keys=True):
        id_2_childs[b][key].append(a)
        
    for a,b,key in graph.out_edges(keys=True):
        id_2_parents[a][key].append(b)

    for id_, data in graph.nodes(data=True):
        synonyms=data.get('synonym')
        categories=list(graph.predecessors('LFID:0000000'))        
        if synonyms:
            for syn in synonyms:

                if 'EXACT' in syn:

                    # Extract the name
                    id_to_synonyms[id_]['EXACT'].append(syn.split('"')[1])

                #elif 'RELATED' in syn:
                else:
                    # Extract the name
                    id_to_synonyms[id_]['RELATED'].append(syn.split('"')[1])
                
    return id_to_name,name_to_id,id_to_synonyms,id_2_childs,id_2_parents
def get_synonyms(lfid,id_to_name,id_to_synonyms):
    #receive a LFID and return name of the LFID and all synonyms as a list
    names=[]
    names.append(id_to_name[lfid])
    synsets=id_to_synonyms[lfid]
    names.extend(synsets['EXACT'])
    names.extend(synsets['RELATED'])
    return names
def generate_lfid_categories2(LSFC_file):
    
    id_to_name,_,id_to_synonyms,_,_=read_LSFC(LSFC_file)
    graph = obonet.read_obo(LSFC_file)
    graph_is_a= copy.deepcopy(graph)
    #We olnly consider is_a relation types initially for making groups and then for untraceble nodes we consider other relation types
    other_edges=[]
    for a,b,key in graph.in_edges(keys=True):
        if key!='is_a':
            other_edges.append((a,b,key))
            #print(a,b,key)
    graph_is_a.remove_edges_from (other_edges)
    # 9 main LSF categories
    categories=list(graph.predecessors('LFID:0000000'))        
    LSF_exisiting_names=[]
    #Assigned category id to each LSF name
    Labels=[]
    Labels_LFIDs=[]
    for lfid in graph.nodes():
        if lfid=='LFID:0000000':
            continue
        T = nx.dfs_postorder_nodes(graph_is_a, source=lfid)   
        ancesstors=list(T)
        # Find category ID
        # ancesstors[0] is root and ancesstors[1] is one of the 9 main LSF categories
        category_id=categories.index(ancesstors[1])
        related_names=get_synonyms(lfid,id_to_name,id_to_synonyms)
        for name in related_names:
            LSF_exisiting_names.append(name)
            Labels.append(category_id)
            Labels_LFIDs.append(name)
            
    return LSF_exisiting_names, Labels,Labels_LFIDs
def generate_lfid_categories(LSFC_file):
    
    id_to_name,_,id_to_synonyms,_,_=read_LSFC(LSFC_file)
    graph = obonet.read_obo(LSFC_file)
    graph_is_a= copy.deepcopy(graph)
    #We olnly consider is_a relation types initially for making groups and then for untraceble nodes we consider other relation types
    other_edges=[]
    for a,b,key in graph.in_edges(keys=True):
        if key!='is_a':
            other_edges.append((a,b,key))
            #print(a,b,key)
    graph_is_a.remove_edges_from (other_edges)
    # 9 main LSF categories
    categories=list(graph.predecessors('LFID:0000000'))        
    LSF_exisiting_names=[]
    #Assigned category id to each LSF name
    Labels=[]
    Labels_LFIDs=[]
    for lfid in graph.nodes():
        if lfid=='LFID:0000000':
            continue
        T = nx.dfs_postorder_nodes(graph_is_a, source=lfid)   
        ancesstors=list(T)
        # Find category ID
        # ancesstors[0] is root and ancesstors[1] is one of the 9 main LSF categories
        category_id=categories.index(ancesstors[1])
        related_names=get_synonyms(lfid,id_to_name,id_to_synonyms)
        for name in related_names:
            LSF_exisiting_names.append(name)
            Labels.append(category_id)
            Labels_LFIDs.append(lfid)
            
    return LSF_exisiting_names, Labels,Labels_LFIDs

def generate_lfid_categories_labels(LSFC_file):
    
    id_to_name,_,id_to_synonyms,_,_=read_LSFC(LSFC_file)
    graph = obonet.read_obo(LSFC_file)
    graph_is_a= copy.deepcopy(graph)
    #We olnly consider is_a relation types initially for making groups and then for untraceble nodes we consider other relation types
    other_edges=[]
    for a,b,key in graph.in_edges(keys=True):
        if key!='is_a':
            other_edges.append((a,b,key))
            #print(a,b,key)
    graph_is_a.remove_edges_from (other_edges)
    # 9 main LSF categories
    categories=list(graph.predecessors('LFID:0000000'))  
    category_names=[id_to_name[cat] for cat in categories]      
    LSF_exisiting_names=[]
    #Assigned category id to each LSF name
    Labels=[]
    Labels_LFIDs=[]
    for lfid in graph.nodes():
        if lfid=='LFID:0000000':
            continue
        T = nx.dfs_postorder_nodes(graph_is_a, source=lfid)   
        ancesstors=list(T)
        # Find category ID
        # ancesstors[0] is root and ancesstors[1] is one of the 9 main LSF categories
        category_id=categories.index(ancesstors[1])
        related_names=get_synonyms(lfid,id_to_name,id_to_synonyms)
        for name in related_names:
            LSF_exisiting_names.append(name)
            Labels.append(category_id)
            Labels_LFIDs.append(lfid)
            
    return LSF_exisiting_names, Labels,Labels_LFIDs,category_names

