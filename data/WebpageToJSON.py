import urllib2
import json
import re


symbols=['H','He','Li','Be','B','C','N','O','F','Ne','Na','Mg','Al','Si','P','S','Cl','Ar','K','Ca','Sc','Ti','V','Cr','Mn','Fe','Co','Ni','Cu','Zn','Ga','Ge','As','Se','Br','Kr','Rb','Sr','Y','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','In','Sn','Sb','Te','I','Xe','Cs','Ba','La','Ce','Pr','Nd','Pm','Sm','Eu','Gd','Tb','Dy','Ho','Er','Tm','Yb','Lu','Hf','Ta','W','Re','Os','Ir','Pt','Au','Hg','Tl','Pb','Bi','Po','At','Rn','Fr','Ra','Ac','Th','Pa','U','Np','Pu','Am','Cm','Bk','Cf','Es','Fm','Md','No','Lr','Rf','Db','Sg','Bh','Hs','Mt','Ds','Rg','Cn']



table=[]

for (Z,sym) in enumerate(symbols,start=1):
    if Z>5: break
    for A in range(1,300):
        if A<(2*Z-10): continue
        if A>(2*Z+70): break
        user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
        headers = { 'User-Agent' : user_agent }
        req = urllib2.Request('http://www.nndc.bnl.gov/nudat2/decaysearchdirect.jsp?nuc='+str(A)+sym+'&unc=standard', None, headers)
        response = urllib2.urlopen(req)
        page = response.read()
        if "No datasets" in page: continue
        print Z,A,sym
        

        nuclide={
            "symbol":sym,
            "Z":Z,
            "A":A,
            "branching":{
                "alpha":0,
                "beta":0
            },
            "Q-value":{
                "alpha":0,
                "beta":0
            },
            "alphabranch":[],
            "betabranch":[],
            "gammabranch":[]
        }
        re_test = re.compile('Decay')
        re_beta_branch = re.compile('&nbsp;&beta;[^0-9]+\-[^0-9]+([0-9.]+)[^%]+%[^0-9]+([0-9.]+)')
        re_beta_branch_implicit = re.compile('&nbsp;&beta;[^0-9]+\-[^0-9:]+([0-9.]+)')
        re_alpha_branch = re.compile('&nbsp;&alpha;[^0-9]+\-[^0-9]+([0-9.]+)[^%]+%[^0-9]+([0-9.]+)')
        re_alpha_branch_implicit = re.compile('&nbsp;alpha;[^0-9]+\-[^0-9:]+([0-9.]+)')
        search_test=re_test.search(page)
        search_alpha_branch=re_alpha_branch.search(page)
        search_beta_branch=re_beta_branch.search(page)
        search_alpha_branch_implicit=re_alpha_branch_implicit.search(page)
        search_beta_branch_implicit=re_beta_branch_implicit.search(page)
        if search_alpha_branch: 
            nuclide["branching"]["alpha"]=search_alpha_branch.group(1)
            nuclide["Q-value"]["alpha"]=search_alpha_branch.group(2)
        if search_beta_branch:
            nuclide["branching"]["beta"]=search_beta_branch.group(1)
            nuclide["Q-value"]["beta"]=search_beta_branch.group(2)
        if search_alpha_branch_implicit: 
            nuclide["branching"]["alpha"]=100
            nuclide["Q-value"]["alpha"]=search_alpha_branch_implicit.group(1)
        if search_beta_branch_implicit:
            nuclide["branching"]["beta"]=100
            nuclide["Q-value"]["beta"]=search_beta_branch_implicit.group(1)
        table.append(nuclide)
        print nuclide
