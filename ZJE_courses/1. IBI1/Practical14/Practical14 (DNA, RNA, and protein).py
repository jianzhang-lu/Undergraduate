import xml.dom.minidom
from xml.dom.minidom import parse
import matplotlib.pyplot as plt

term_list=[]
DOMTree = xml.dom.minidom.parse('go_obo.xml')
obo = DOMTree.documentElement
terms = obo.getElementsByTagName('term')
is_a_dictionary = {}
count = 0
for term in terms:
    if term.getElementsByTagName('is_a'):
        is_a_length = len(term.getElementsByTagName('is_a'))
        # get the child nodes
        term_id = term.getElementsByTagName('id')[0].childNodes[0].data
        # get the father nodes
        while count < is_a_length:
            term_is_a = term.getElementsByTagName('is_a')[count].childNodes[0].data
            if term_is_a not in is_a_dictionary:
                is_a_dictionary[term_is_a] = [term_id]
            else:
                is_a_dictionary[term_is_a].append(term_id)
            count += 1
    count = 0

'''new_is_a_dictionary is the dictionary to store the information of fathers and children 
    (all terms). The key is the fathers, and the value is the list of children.'''

def get_specific_terms(organics):
    specific_terms_list = []
    for term1 in terms:
        content = term1.getElementsByTagName('defstr')[0].childNodes[0].data
        if organics == 'RNA' or organics == 'DNA':
            real_content = content
        else:
            real_content = content.upper()
        if organics in real_content:
            organics_id = term1.getElementsByTagName('id')[0].childNodes[0].data
            specific_terms_list.append(organics_id)
    return specific_terms_list

children_list = []

def get_next_children(need_list):
    next_generation = []
    for every_need_id in need_list:
        if every_need_id in is_a_dictionary:
            children_list.extend(is_a_dictionary[every_need_id])
            next_generation.extend(is_a_dictionary[every_need_id])

    test = next_generation[:]
    if next_generation == []:
        return len(set(children_list))
    else:
        return get_next_children(test)

DNA_terms_list = get_specific_terms('DNA')
a = get_next_children(DNA_terms_list)
children_list = []
print('The childNodes of DNA is:', a)

RNA_terms_list = get_specific_terms('RNA')
b = get_next_children(RNA_terms_list)
children_list = []
print('The childNodes of RNA is:', b)

protein_terms_list = get_specific_terms('PROTEIN')
c = get_next_children(protein_terms_list)
children_list = []
print('The childNodes of protein is:', c)

# the fourth organics I choose is carbohydrate.
carbohydrate_terms_list = get_specific_terms('CARBOHYDRATE')
d = get_next_children(carbohydrate_terms_list)
children_list = []
print('The childNodes of carbohydrate is:', d)

labels = 'DNA', 'RNA', 'protein', 'carbohydrate'
sizes = [a,b,c,d]
explode = (0.1, 0, 0, 0)
plt.pie(sizes, explode=explode, labels=labels, autopct='%1.2f%%', shadow=False, startangle=90)
plt.title('Practical 14')
plt.axis('equal')
plt.show()