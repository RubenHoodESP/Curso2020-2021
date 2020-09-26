# -*- coding: utf-8 -*-
"""Task07.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tV5j-DRcpPtoJGoMj8v2DSqR_9wyXeiE

**Task 07: Querying RDF(s)**
"""

github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2020-2021/master/Assignment4"

"""Leemos el fichero RDF de la forma que lo hemos venido haciendo"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/resources/example6.rdf", format="xml")

ns = Namespace("http://somewhere#")
rstr = "RDFLib mode"
sstr = "SPARQL mode"

print("TASK 7")

"""**TASK 7.1: List all subclasses of "Person" with RDFLib and SPARQL**"""

print(rstr)

for s,p,o in g.triples((None, RDFS.subClassOf, ns.Person)):
    print(s)

print(sstr)

from rdflib.plugins.sparql import prepareQuery

q1 = prepareQuery('''
    SELECT 
        ?Subject
    WHERE {
        ?Subject rdfs.subClassOf ns.Person.
    }
    ''',
    initNs = {"rdfs":RDFS, "ns":ns}
)

for s in g.query(q1):
    print(s)


"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**"""

print("TASK 7.2")
print(rstr)

subclasses = []
for s,p,o in g.triples((None, RDFS.subClassOf, ns.Person)):
    subclasses.append(s)
for s,p,o in g.triples((None, RDF.type, ns.Person)):
    print(s)
for subclass in subclasses:
    for s,p,o in g.triples((None, RDF.type, subclass)):
        print(s)

print(sstr)

q2 = prepareQuery('''
    SELECT
        ?Subject
    WHERE {
        ?Subject (rdf:type/rdfs::subClassOf*) ns.Person .
    }
    ''',
    initNs = {"rdf":RDF, "rdfs":RDFS, "ns":ns}
)

for s in g.query(q2):
    print(s)


"""**TASK 7.3: List all individuals of "Person" and all their properties including their class with RDFLib and SPARQL**"""

print("TASK 7.3")
print(rstr)

for s1,p1,o1 in g.triples((None, RDF.type, ns.Person)):
    for s2,p2,o2 in g.triples((s1, None, None)):
        print(s1, p2, o2)

for s1,p1,o1 in g.triples((None, RDF.type, subclasses)):
    for s2,p2,o2 in g.triples((s1, None, None)):
        print(s1, p2, o2)

print(sstr)

q3 = prepareQuery('''
    SELECT
        ?S ?P ?O
    WHERE {
        ?S (rdf:type/rdfs::subClassOf*) ns.Person .
        ?S ?P ?O
    }
    ''',
    initNs = {"rdf":RDF, "rdfs":RDFS, "ns":ns}
)

for s in g.query(q3):
    print(s)
