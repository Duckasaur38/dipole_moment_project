import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

st.markdown(
    r'''**
    enter a chemical formula below. it should have the following format (no quotes 😊)**''')
st.code(" 'charge,symbol number, ..., symbol number, center' ")
st.markdown(" ** make sure to seperate each element with a comma, and don't forget to tell us the charge first (even if its 0) and the central atom as the final symbol. for example, $CH_4$ should be entered as **") 
st.code(" '0,C1,H4,C' ")
input_formula = st.text_input('formula', value='', max_chars=None, key=None, type='default')
st.markdown("_** LP means lone pair. if you don't see a blue vector, that means its on top of a bond. happy dipoling**_")

path = '/Users/zoeshleifer/Census-Data-Streamlit-App/periodic_table.csv'
ptable = pd.read_csv(path)
ptable.set_index('Symbol')

def formula_list(formula_str):
        form_list = []
        comma_split = formula_str.split(',')
        charge = -int(comma_split[0])
        for chem in comma_split[1:-1]:
            num = (int(''.join(c for c in chem if c.isdigit())))
            form_list.append(num *[(chem.replace(''.join(c for c in chem if c.isdigit()),''))])
        form_list = sum(form_list,[])
        form_list.insert(0, form_list.pop(form_list.index(comma_split[-1])))
        total_v = 0
        hy = 0
        for chem in form_list:
            total_v += ptable.set_index('Symbol')['NumberofValence'].loc[chem]
            if chem == 'H':
                hy +=1
        pairs = int((charge + total_v - 8*(len(form_list)-1-hy) - 2*hy)/2)
        form_list += (pairs*['LP'])
        return form_list
def comp_en_diffs(formula_lst): 
    en_diff = []
    c_en = ptable.set_index('Symbol')['Electronegativity'].loc[formula_lst[0]]
    for i in formula_lst[1:]:
        if i == 'LP':
            en_diff.append(0)
        else:
            en_diff.append(abs(c_en - ptable.set_index('Symbol')['Electronegativity'].loc[i]))
    return en_diff
def compute_dipole(unit_vectors, en_diffs):
    dipole_vector = []
    for i in range(0,len(unit_vectors)):
        dipole_vector.append(tuple(np.array(unit_vectors[i])*en_diffs[i]))
    vector_list = zip(*dipole_vector)
    dipole_vector = []
    for thing in vector_list:
        dipole_vector.append(sum(thing))
    return dipole_vector

def bond_plt(formula_str):
    label4 = [[0, 0, 6],[4, 4, -.2],[-5, 5, -1],[0, -6, -3]]
    label3 = [[0,0,3.5],[-7,1,-4],[3,3,-1]]
    label2 = [[6.5,-4,3.5],[-7,4,-2]]
    label1 = [[6,-4,3]]
    label0 = [[0,0,0]]
    scalar = [3,3,4,5,8]
    big_lab = [label0,label1,label2,label3,label4]
    unit_vectors4 =[[0,0,np.sqrt(6)/4],[.5,np.sqrt(3)/3,-np.sqrt(6)/12],[-.5,np.sqrt(3)/3,-np.sqrt(6)/12],[0,-np.sqrt(3)/3,-np.sqrt(6)/12]]
    unit_vectors3 = [[-.5,.866,0],[-.5,-.866,0],[1,0,0]]
    unit_vectors2 = [[1,0,0],[-1,0,0]]
    unit_vectors1 = [[1,0,0]]
    unit_vectors0 = []
    big_vec = [unit_vectors0,unit_vectors1,unit_vectors2,unit_vectors3,unit_vectors4]

    formula = formula_list(formula_str)
    en_diffs = comp_en_diffs(formula)
    size = len(en_diffs)
    vectors = big_vec[size]
    labels = big_lab[size]
    vectors.append(compute_dipole(vectors,en_diffs))
    for vector in vectors:
        for i in range(0,3): vector.insert(0,0)
    soa = scalar[size]*np.array(vectors)
    X, Y, Z, U, V, W = zip(*soa)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.quiver(X[:-1], Y[:-1], Z[:-1], U[:-1], V[:-1], W[:-1],color='r',arrow_length_ratio=0.0001)
    ax.quiver(X[-1], Y[-1], Z[-1], U[-1], V[-1], W[-1],color='b',arrow_length_ratio=0.1)
    for i in range(size):
        ax.text(*labels[i],formula[i+1], color='red')
    bounds = [[-5,5],[-5,5],[-5,5]]
    ax.set_xlim(bounds[0])
    ax.set_ylim(bounds[1])
    ax.set_zlim(bounds[2])
    plt.show()
bond_plt(input_formula)
st.pyplot()
