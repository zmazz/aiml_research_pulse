import requests

#import datetime
import streamlit as st
import pandas as pd
import seaborn as sns
#import numpy as np
import matplotlib.pyplot as plt
#import plotly.express as px
#import research_pulse.logic.search as ls
#import research_pulse.logic.data_loader as ldl
#import research_pulse.logic.analytics_agg as laa
import streamlit.components.v1 as components

import pandas as pd
from collections import defaultdict
import numpy as np
# PDF display imports
from base64 import b64encode
from io import BytesIO
import urllib3
from pdf2image import convert_from_bytes
#from PIL import Image
#from io import StringIO
import json


# Load app data from JSON file
def load_data():
    with open("research_pulse/interface/app_data.json", "r") as f:
        data = json.load(f)
    return data

# Save updated app data to JSON file
def save_data(data):
    with open("research_pulse/interface/app_data.json", "w") as f:
        json.dump(data, f)

# Increment page views
def increment_page_views(data):
    data["page_views"] += 1
    save_data(data)

# Load app data
data = load_data()

# Initialize session state
if "page_viewed" not in st.session_state:
    st.session_state.page_viewed = False

# Increment and display page views
if not st.session_state.page_viewed:
    increment_page_views(data)
    st.session_state.page_viewed = True




st.set_page_config(
    page_title="Research Pulse",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/zmazz/aiml_research_pulse',
        'Report a bug': "https://github.com/zmazz/aiml_research_pulse",
        'About': "AI, ML and related research areas are evolving at a rapid pace. Research Pulse is a tool that helps you to explore the research papers and their authors. It is a NLP tool that helps you to find the most relevant papers and authors in your research area. For more info, please contact https://github.com/zmazz."
    }
)

#@st.cache_data
#def load_data():
#    data=ldl.load_data()
#    return data

#df=load_data()

html_temp = """
            <div style="background-color:{};padding:1px">
            </div>
            """

st.markdown(
    f"""
    <style>
        /* Center all text in Streamlit page */
        .stApp {{
            text-align: center;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# 3 research_authors functions
def author_mean_pub_freq(dic, author):
    # conversion du dictionnaire en DataFrame
    df = pd.DataFrame.from_dict(dic, orient='index', columns=['Title', 'Authors', 'Id', 'Year', 'Link', 'Category', 'Number_citations', 'Abstract'])
    # conversion de la colonnée Year en format int
    df['Year'] = df['Year'].astype(int)
    # Create a dictionary to store the publication counts for each author and year
    author_year_count = defaultdict(lambda: defaultdict(int))
    # Loop over each row in the dataframe and update the publication count for each author and year
    for _, row in df.iterrows():
        authors = row['Authors'].split(', ')
        year = row['Year']
        for auth in authors:
            author_year_count[auth][year] += 1
    # Create a new dataframe to store the results
    author_publication_freq = pd.DataFrame(columns=['author', 'year', 'num_publications'])
    # Convert the column num_publications format from string to integer format
    author_publication_freq['num_publications'] = author_publication_freq['num_publications'].astype(int)
    # Loop over the author-year counts and add them to the new dataframe
    for auth, year_counts in author_year_count.items():
        for year, count in year_counts.items():
            author_publication_freq = pd.concat([author_publication_freq, pd.DataFrame({'author': [auth], 'year': [year], 'num_publications': [count]})], ignore_index=True)
    # Check if the author filled by the user is present on the dataframe author_df
    author_df = author_publication_freq.loc[author_publication_freq['author'].str.contains(author)]
    if author_df.empty:
            return(f"The author {author} could not be found. Please fill in the last name followed by the first name of the author.")
    # Check if the author filled by the user is present on the dataframe author_df
    first_year = author_df['year'].min()
    last_year = author_df['year'].max()
    num_years = last_year - first_year + 1
    total_publications = author_df['num_publications'].sum()
    mean_freq = total_publications / num_years
    return(f'Between his/her first year ({first_year}) and last year ({last_year}) of publication, {author} has published {total_publications} papers, on an average of {round(mean_freq,1)} papers per year.')

def get_author_citation_frequency(dic, author):

    # conversion du dictionnaire en DataFrame
    df = pd.DataFrame.from_dict(dic, orient='index', columns=['Title', 'Authors', 'Id', 'Year', 'Link', 'Category', 'Number_citations', 'Abstract'])

    # conversion de la colonnée Year en format int
    df['Year'] = df['Year'].astype(int)
    df['Number_citations'] = df['Number_citations'].astype(int)



    author_stats = pd.DataFrame(columns=['author', 'year', 'num_publications', 'num_citations'])
    # Convert the column num_publications format from string to integer format
    author_stats['num_publications'] = author_stats['num_publications'].astype(int)

    for index, row in df.iterrows():
        authors = row['Authors'].split(', ')
        year = row['Year']
        num_citations = row['Number_citations']
        for aut in authors:
            temp_df = pd.DataFrame({'author': [aut], 'year': [year], 'num_publications': [1], 'num_citations': [num_citations]})
            author_stats = pd.concat([author_stats, temp_df], ignore_index=True)
    author_stats = author_stats.groupby(['author', 'year']).agg({'num_publications': 'sum', 'num_citations': 'sum'}).reset_index()
    author_stats = author_stats[['author', 'year', 'num_publications', 'num_citations']]

    # Vérifier si l'auteur est présent dans le dataframe
    if author_stats['author'].str.contains(author).sum() == 0 :
        return f"The author {author} could not be found. Please fill in the last name followed by the first name of the author."

    # Filtrer les publications de l'auteur
    author_publications = author_stats.loc[author_stats['author'].str.contains(author)]
    # Calculer la première et la dernière année de publication de l'auteur
    first_year = author_publications['year'].min()
    last_year = author_publications['year'].max()
    # Créer un tableau de fréquences de citations pour chaque année de publication
    citation_frequencies = np.zeros(last_year-first_year+1)
    for year in range(first_year, last_year+1):
        publications_in_year = author_publications[author_publications['year'] == year]
        if not publications_in_year.empty:
            citation_frequencies[year-first_year] = publications_in_year['num_citations'].sum() / publications_in_year['num_publications'].sum()
    # Calculer la moyenne pondérée des fréquences de citation
    weighted_sum = 0
    total_weight = 0
    for i, freq in enumerate(citation_frequencies):
        weight = author_publications[author_publications['year'] == first_year+i]['num_publications'].sum()
        weighted_sum += freq * weight
        total_weight += weight
    mean_weighted_frequency = weighted_sum / total_weight
    # Créer un DataFrame avec les résultats
    result = pd.DataFrame({'author': [author],
                           'mean_weighted_citation_frequency': [mean_weighted_frequency]})
    # Le DataFrame avec les résultats ne contient qu'une ligne, avec l'auteur et la fréquence associée
    # On ne choisit d'afficher que la valeur ci-dessous

    return f'In that time, he/she was cited {weighted_sum} times, on average {round(result["mean_weighted_citation_frequency"][0])} times per year.'

def get_collaboration_citation_frequency_stats_V2(dic,author):


    # conversion du dictionnaire en DataFrame
    df = pd.DataFrame.from_dict(dic, orient='index', columns=['Title', 'Authors', 'Id', 'Year', 'Link', 'Category', 'Number_citations', 'Abstract'])

    # conversion de la colonnée Year en format int
    df['Year'] = df['Year'].astype(int)
    df['Number_citations'] = df['Number_citations'].astype(int)

    # Créer un dictionnaire pour stocker les statistiques de collaboration
    collab_stats = {}

    # Itérer sur chaque publication
    for index, row in df.iterrows():
        # Extraire les informations nécessaires pour chaque publication
        authors = row['Authors'].split(", ")
        year = row['Year']
        num_publications = 1
        num_citations = row['Number_citations']

        # Ajouter les informations à l'entrée de chaque collaboration
        if len(authors) >= 2:
            for i in range(len(authors)):
                for j in range(i+1, len(authors)):
                    collab = tuple(sorted([authors[i], authors[j]]))
                    if collab not in collab_stats:
                        collab_stats[collab] = {'year': [], 'num_publications': [], 'num_citations': []}
                    collab_stats[collab]['year'].append(year)
                    collab_stats[collab]['num_publications'].append(num_publications)
                    collab_stats[collab]['num_citations'].append(num_citations)

    # Créer un dataframe à partir des statistiques de collaboration
    result = pd.DataFrame(columns=['collaboration', 'year', 'num_publications', 'num_citations'])
    for collab in collab_stats:
        years = collab_stats[collab]['year']
        num_pubs = collab_stats[collab]['num_publications']
        num_cits = collab_stats[collab]['num_citations']
        for i in range(len(years)):
            temp_df = pd.DataFrame({'collaboration': [collab], 'year': [years[i]], 'num_publications': [num_pubs[i]], 'num_citations': [num_cits[i]]})
            result = pd.concat([result, temp_df], ignore_index=True)


    # Create a dictionary to store collaboration citation frequency
    collab_citation_freq = {}

    # Iterate over each collaboration
    for index, row in result.iterrows():
        # Extract information for each collaboration
        collab = row['collaboration']
        year = row['year']
        num_pubs = row['num_publications']
        num_cits = row['num_citations']

        # Add information to the entry of each collaboration
        if len(collab) > 1:
            for i in range(len(collab)):
                for j in range(i+1, len(collab)):
                    authors = tuple(sorted([collab[i], collab[j]]))
                    if authors not in collab_citation_freq:
                        collab_citation_freq[authors] = {'num_pubs': [], 'num_cits': []}
                    collab_citation_freq[authors]['num_pubs'].append(num_pubs)
                    collab_citation_freq[authors]['num_cits'].append(num_cits)

    # Calculate the mean weighted citation frequency for each collaboration
    collab_mean_weighted_cit_freq = {}
    for collab in collab_citation_freq:
        num_pubs = collab_citation_freq[collab]['num_pubs']
        num_cits = collab_citation_freq[collab]['num_cits']
        total_weight = sum(num_pubs)
        weighted_sum = sum([num_cits[i] * num_pubs[i] for i in range(len(num_pubs))])
        if total_weight > 0:
            mean_weighted_cit_freq = weighted_sum / total_weight
        else:
            mean_weighted_cit_freq = 0
        collab_mean_weighted_cit_freq[collab] = mean_weighted_cit_freq

    # Convert the dictionary to a dataframe and sort by mean weighted citation frequency
    result_2 = pd.DataFrame({'collaboration': list(collab_mean_weighted_cit_freq.keys()),
                           'mean_weighted_citation_frequency': list(collab_mean_weighted_cit_freq.values())})
    result_2['mean_weighted_citation_frequency'].fillna(0, inplace=True)
    result_2.sort_values(by='mean_weighted_citation_frequency', ascending=False, inplace=True)


    # Check if the author filled by the user is present on the 'dataframe result_2'
    if result_2[result_2['collaboration'].apply(lambda x: author in x)].shape[0] == 0:
        return f"The author {author} is not part of any collaboration. "

    # In the case she/he is part of collaboration, we display the results by displaying the dataframe result_2 with the author's name
    # with a visualization output
    else:

        final_result = result_2[result_2['collaboration'].apply(lambda x: author in x)]
        df_sorted = final_result.sort_values(by='mean_weighted_citation_frequency', ascending=False)
        # Extract collaboration names and citation frequencies
        collaborations = df_sorted['collaboration'].apply(lambda x: f'{x[0]} & {x[1]}')
        citation_frequencies = df_sorted['mean_weighted_citation_frequency']

        # Set seaborn style
        sns.set_style("whitegrid")


        # Create horizontal bar plot using seaborn
        fig, ax = plt.subplots(figsize=(10, 6))
        ax = sns.barplot(x=citation_frequencies, y=collaborations, color='steelblue', ax=ax)

        # Add labels and titles
        ax.set_xlabel('Annual Mean Citation Frequency', fontsize=14, fontweight='bold')
        ax.set_ylabel('Collaborations', fontsize=14, fontweight='bold')
        ax.set_title(f'Average annual frequency of citation for each collaboration involving {author}', fontsize=16, fontweight='bold')

        # Customize tick labels
        ax.set_xticklabels(ax.get_xticklabels(), fontsize=12)
        ax.set_yticklabels(ax.get_yticklabels(), fontsize=12)

        # Remove spines
        sns.despine(left=True, bottom=True)

        # Add annotations to the bars
        for i, v in enumerate(citation_frequencies):
            ax.text(v+0.05, i, f'{v:.2f}', fontsize=12, fontweight='bold')

        # Show the plot
        plt.tight_layout()
        plt.close(fig)

        # Retournez l'objet figure à la fin de la fonction
        return fig

# 2 dashboard data below
top100_papers={'title': {'1004-3169': 'Factorizations of Cunningham numbers with bases 13 to 99',
  '1612-07324': 'Holographic quantum matter',
  '1101-0618': 'Gauge/String Duality, Hot QCD and Heavy Ion Collisions',
  '1712-03107': 'Dynamical systems applied to cosmology: dark energy and modified gravity',
  '801-2826': 'Non-Commutative Geometry, Categories and Quantum Physics',
  '1503-00732': 'Quantum field theory in a magnetic field: From quantum chromodynamics to\n  graphene and Dirac semimetals',
  '1805-04405': 'The Conformal Bootstrap: Theory, Numerical Techniques, and Applications',
  '1712-05815': 'Relativistic Fluid Dynamics In and Out of Equilibrium -- Ten Years of\n  Progress in Theory and Numerical Simulations of Nuclear Collisions',
  '1302-028': 'Holographic applications of logarithmic conformal field theories',
  '1106-1445': 'From Classical to Quantum Shannon Theory',
  '1909-11512': 'Synthetic Data for Deep Learning',
  '1204-245': 'Entanglement Entropy from a Holographic Viewpoint',
  '1302-0884': 'Scale invariance vs conformal invariance',
  '1804-06469': 'Bayesian parameter estimation for relativistic heavy-ion collisions',
  '1812-02893': 'The Calabi-Yau Landscape: from Geometry, to Physics, to Machine-Learning',
  '1903-05082': 'Machine Learning Solutions for High Energy Physics: Applications to\n  Electromagnetic Shower Generation, Flavor Tagging, and the Search for\n  di-Higgs Production',
  '1610-08526': 'BMS Particles in Three Dimensions',
  '1711-00394': 'Universal gradient descent',
  '1003-1366': 'Fundamentals of the Exact Renormalization Group',
  '1104-3712': 'Entanglement entropy of black holes',
  '1710-08425': 'Hydrodynamics of electrons in graphene',
  '1410-8712': 'Functional renormalisation approach to driven dissipative dynamics',
  '1003-4725': 'Quantum integrability and functional equations',
  '1903-10563': 'Machine learning and the physical sciences',
  '1805-06467': 'Top Down Approach to 6D SCFTs',
  '1912-06855': 'Planar maps and random partitions',
  '1901-05895': 'Bipartite Quantum Interactions: Entangling and Information Processing\n  Abilities',
  '1511-04265': 'Eisenstein series and automorphic representations',
  '1606-08953': 'TASI lectures on quantum matter (with a view toward holographic duality)',
  '1807-03334': 'An introduction to the SYK model',
  '905-0932': 'Holographic Entanglement Entropy: An Overview',
  '1409-1178': 'Horava-Lifshitz Gravity and Effective Theory of the Fractional Quantum\n  Hall Effect',
  '1909-02005': 'Mining for Dark Matter Substructure: Inferring subhalo population\n  properties from strong lenses with machine learning',
  '2002-12187': 'Pedagogical introduction to SYK model and 2D Dilaton Gravity',
  '905-4013': 'Entanglement entropy and conformal field theory',
  '1803-08823': 'A high-bias, low-variance introduction to Machine Learning for\n  physicists',
  '1803-01164': 'The History Began from AlexNet: A Comprehensive Survey on Deep Learning\n  Approaches',
  '1908-02667': 'A Practical Mini-Course on Applied Holography',
  '2001-06937': 'A Review on Generative Adversarial Networks: Algorithms, Theory, and\n  Applications',
  '1910-04713': 'Mating of trees for random planar maps and Liouville quantum gravity: a\n  survey',
  '1603-09741': 'Demystifying the Holographic Mystique',
  '1409-3575': 'AdS/CFT Duality User Guide',
  '1805-12137': 'Resurgence and Lefschetz thimble in 3d N=2 supersymmetric Chern-Simons\n  matter theories',
  '1903-00491': 'Conformal field theory and the hot phase of three-dimensional U(1) gauge\n  theory',
  '1912-04977': 'Advances and Open Problems in Federated Learning',
  '1905-10378': 'Jackiw-Teitelboim Gravity and Rotating Black Holes',
  '1811-1256': 'An Introduction to Deep Reinforcement Learning',
  '1907-04332': 'Subsystem trace distance in low-lying states of (1+1)-dimensional\n  conformal field theories',
  '1908-00013': 'Mirror symmetry and line operators',
  '1903-06633': 'Phases Of Melonic Quantum Mechanics',
  '1110-3814': 'Lectures on holographic non-Fermi liquids and quantum phase transitions',
  '1311-7565': 'Time evolution as refining, coarse graining and entangling',
  '806-3474': 'Information field theory for cosmological perturbation reconstruction\n  and non-linear signal analysis',
  '1312-6689': 'Quantum geometry and quiver gauge theories',
  '1712-08016': '(q,t)-KZ equations for quantum toroidal algebra and Nekrasov partition\n  functions on ALE spaces',
  '1901-07038': 'Physics of eccentric binary black hole mergers: A numerical relativity\n  perspective',
  '1912-02047': 'Neural Machine Translation: A Review and Survey',
  '1611-07053': 'Second-order transport, quasinormal modes and zero-viscosity limit in\n  the Gauss-Bonnet holographic fluid',
  '1711-07982': 'Symmetry-enriched topological order in tensor networks: Defects, gauging\n  and anyon condensation',
  '1604-05544': 'Jarzynskis theorem for lattice gauge theory',
  '1908-09858': 'Anomalies, a mod 2 index, and dynamics of 2d adjoint QCD',
  '1610-03911': 'Zoo of quantum-topological phases of matter',
  '1210-054': 'Hyperscaling violation : a unified frame for effective holographic\n  theories',
  '1912-08957': 'Optimization for deep learning: theory and algorithms',
  '1912-01006': '4d/2d rightarrow  3d/1d: A song of protected operator algebras',
  '1608-05351': 'Toric Calabi-Yau threefolds as quantum integrable systems. R-matrix and\n  RTT relations',
  '1810-01185': 'Adversarial Examples - A Complete Characterisation of the Phenomenon',
  '1801-08156': 'Fluctuations in cool quark matter and the phase diagram of Quantum\n  Chromodynamics',
  '1211-1273': 'General Lagrangian Formulation for Higher Spin Fields with Arbitrary\n  Index Symmetry. 2. Fermionic fields',
  '1603-08382': 'Boundaries, Mirror Symmetry, and Symplectic Duality in 3d\n  mathcalN=4 Gauge Theory',
  '2002-05442': 'Deep Learning for Source Code Modeling and Generation: Models,\n  Applications and Challenges',
  '1801-00553': 'Threat of Adversarial Attacks on Deep Learning in Computer Vision: A\n  Survey',
  '1808-09434': 'TASI Lectures on Large N Tensor Models',
  '1807-08169': 'Recent Advances in Deep Learning: An Overview',
  '1809-03193': 'Recent Advances in Object Detection in the Age of Deep Convolutional\n  Neural Networks',
  '1410-6201': 'Nonlocal probes of thermalization in holographic quenches with spectral\n  methods',
  '1802-09439': 'Cosmological constant from condensation of defect excitations',
  '1910-10045': 'Explainable Artificial Intelligence (XAI): Concepts, Taxonomies,\n  Opportunities and Challenges toward Responsible AI',
  '1706-04054': 'Inverse Bootstrapping Conformal Field Theories',
  '1808-09072': 'Holographic Spacetimes as Quantum Circuits of Path-Integrations',
  '1904-02704': 'Chiral Algebra, Localization, Modularity, Surface defects, And All That',
  '1110-5044': 'General Lagrangian Formulation for Higher Spin Fields with Arbitrary\n  Index Symmetry. I. Bosonic fields',
  '1401-7788': 'New developments for dual methods in lattice field theory at non-zero\n  density',
  '1809-07294': 'Generative Adversarial Network in Medical Imaging: A Review',
  '1910-03584': 'Long-lived interacting phases of matter protected by multiple\n  time-translation symmetries in quasiperiodically-driven systems',
  '1911-05741': 'From VOAs to short star products in SCFT',
  '1801-05416': 'Tunneling Topological Vacua via Extended Operators: (Spin-)TQFT Spectra\n  and Boundary Deconfinement in Various Dimensions',
  '1807-11939': 'Entanglement cost and quantum channel simulation',
  '1810-05165': 'Energy Flow Networks: Deep Sets for Particle Jets',
  '1912-03324': 'Carving out OPE space and precise O(2) model critical exponents',
  '1902-09166': 'Anomaly-induced transport phenomena from the imaginary-time formalism',
  '1603-0877': 'Universality of anomalous conductivities in theories with\n  higher-derivative holographic duals',
  '1905-02191': 'Entanglement Entropy, OTOC and Bootstrap in 2D CFTs from Regge and Light\n  Cone Limits of Multi-point Conformal Block',
  '1910-03883': 'Second-order coding rates for key distillation in quantum key\n  distribution',
  '1611-07304': 'Anomaly in RTT relation for DIM algebra and network matrix models',
  '1706-03044': 'Complete random matrix classification of SYK models with\n  mathcalN=0, 1 and 2 supersymmetry',
  '1303-2287': 'Topological Many-Body States in Quantum Antiferromagnets via Fuzzy\n  Super-Geometry',
  '1301-198': 'Quivers as Calculators: Counting, Correlators and Riemann Surfaces',
  '1809-00736': '3d Mirror Symmetry from S-duality',
  '1202-6062': 'Schrodinger Holography with and without Hyperscaling Violation'},
 'author(s)': {'1004-3169': 'Brent Richard P., Montgomery Peter L., Riele Herman J. J. te',
  '1612-07324': 'Hartnoll Sean A., Lucas Andrew, Sachdev Subir',
  '1101-0618': 'Casalderrey-Solana Jorge, Liu Hong, Mateos David, Rajagopal Krishna, Wiedemann Urs Achim',
  '1712-03107': 'Bahamonde Sebastian, Boehmer Christian G., Carloni Sante, Copeland Edmund J., Fang Wei, Tamanini Nicola',
  '801-2826': 'Bertozzini Paolo, Conti Roberto, Lewkeeratiyutkul Wicharn',
  '1503-00732': 'Miransky Vladimir A., Shovkovy Igor A.',
  '1805-04405': 'Poland David, Rychkov Slava, Vichi Alessandro',
  '1712-05815': 'Romatschke Paul, Romatschke Ulrike',
  '1302-028': 'Grumiller D., Riedler W., Rosseel J., Zojer T.',
  '1106-1445': 'Wilde Mark M.',
  '1909-11512': 'Nikolenko Sergey I.',
  '1204-245': 'Takayanagi Tadashi',
  '1302-0884': 'Nakayama Yu',
  '1804-06469': 'Bernhard Jonah E.',
  '1812-02893': 'He Yang-Hui',
  '1903-05082': 'Paganini Michela',
  '1610-08526': 'Oblak Blagoje',
  '1711-00394': 'Gasnikov Alexander',
  '1003-1366': 'Rosten Oliver J.',
  '1104-3712': 'Solodukhin Sergey N.',
  '1710-08425': 'Lucas Andrew, Fong Kin Chung',
  '1410-8712': 'Mathey Steven',
  '1003-4725': 'Volin Dmytro',
  '1903-10563': 'Carleo Giuseppe, Cirac Ignacio, Cranmer Kyle, Daudet Laurent, Schuld Maria, Tishby Naftali, Vogt-Maranto Leslie, Zdeborová Lenka',
  '1805-06467': 'Heckman Jonathan J., Rudelius Tom',
  '1912-06855': 'Bouttier Jérémie',
  '1901-05895': 'Das Siddhartha',
  '1511-04265': 'Fleig Philipp, Gustafsson Henrik P. A., Kleinschmidt Axel, Persson Daniel',
  '1606-08953': 'McGreevy John',
  '1807-03334': 'Rosenhaus Vladimir',
  '905-0932': 'Nishioka Tatsuma, Ryu Shinsei, Takayanagi Tadashi',
  '1409-1178': 'Wu Chaolun, Wu Shao-Feng',
  '1909-02005': 'Brehmer Johann, Mishra-Sharma Siddharth, Hermans Joeri, Louppe Gilles, Cranmer Kyle',
  '2002-12187': 'Trunin Dmitrii A.',
  '905-4013': 'Calabrese Pasquale, Cardy John',
  '1803-08823': 'Mehta Pankaj, Bukov Marin, Wang Ching-Hao, Day Alexandre G. R., Richardson Clint, Fisher Charles K., Schwab David J.',
  '1803-01164': 'Alom Md Zahangir, Taha Tarek M., Yakopcic Christopher, Westberg Stefan, Sidike Paheding, Nasrin Mst Shamima, Van Esesn Brian C, Awwal Abdul A S., Asari Vijayan K.',
  '1908-02667': 'Baggioli Matteo',
  '2001-06937': 'Gui Jie, Sun Zhenan, Wen Yonggang, Tao Dacheng, Ye Jieping',
  '1910-04713': 'Gwynne Ewain, Holden Nina, Sun Xin',
  '1603-09741': 'Khveshchenko D. V.',
  '1409-3575': 'Natsuume Makoto',
  '1805-12137': 'Fujimori Toshiaki, Honda Masazumi, Kamata Syo, Misumi Tatsuhiro, Sakai Norisuke',
  '1903-00491': 'Caselle Michele, Nada Alessandro, Panero Marco, Vadacchino Davide',
  '1912-04977': 'Kairouz Peter, McMahan H. Brendan, Avent Brendan, Bellet Aurélien, Bennis Mehdi, Bhagoji Arjun Nitin, Bonawitz Kallista, Charles Zachary, Cormode Graham, Cummings Rachel, DOliveira Rafael G. L., Eichner Hubert, Rouayheb Salim El, Evans David, Gardner Josh, Garrett Zachary, Gascón Adrià, Ghazi Badih, Gibbons Phillip B., Gruteser Marco, Harchaoui Zaid, He Chaoyang, He Lie, Huo Zhouyuan, Hutchinson Ben, Hsu Justin, Jaggi Martin, Javidi Tara, Joshi Gauri, Khodak Mikhail, Konečný Jakub, Korolova Aleksandra, Koushanfar Farinaz, Koyejo Sanmi, Lepoint Tancrède, Liu Yang, Mittal Prateek, Mohri Mehryar, Nock Richard, Özgür Ayfer, Pagh Rasmus, Raykova Mariana, Qi Hang, Ramage Daniel, Raskar Ramesh, Song Dawn, Song Weikang, Stich Sebastian U., Sun Ziteng, Suresh Ananda Theertha, Tramèr Florian, Vepakomma Praneeth, Wang Jianyu, Xiong Li, Xu Zheng, Yang Qiang, Yu Felix X., Yu Han, Zhao Sen',
  '1905-10378': 'Moitra Upamanyu, Sake Sunil Kumar, Trivedi Sandip P., Vishal V.',
  '1811-1256': 'Francois-Lavet Vincent, Henderson Peter, Islam Riashat, Bellemare Marc G., Pineau Joelle',
  '1907-04332': 'Zhang Jiaju, Ruggiero Paola, Calabrese Pasquale',
  '1908-00013': 'Dimofte Tudor, Garner Niklas, Geracie Michael, Hilburn Justin',
  '1903-06633': 'Ferrari Frank, Massolo Fidel I. Schaposnik',
  '1110-3814': 'Iqbal Nabil, Liu Hong, Mezei Márk',
  '1311-7565': 'Dittrich Bianca, Steinhaus Sebastian',
  '806-3474': 'Ensslin Torsten A., Frommert Mona, Kitaura Francisco S.',
  '1312-6689': 'Nekrasov Nikita, Pestun Vasily, Shatashvili Samson',
  '1712-08016': 'Awata H., Kanno H., Mironov A., Morozov A., Suetake K., Zenkevich Y.',
  '1901-07038': 'Huerta E. A., Haas Roland, Habib Sarah, Gupta Anushri, Rebei Adam, Chavva Vishnu, Johnson Daniel, Rosofsky Shawn, Wessel Erik, Agarwal Bhanu, Luo Diyu, Ren Wei',
  '1912-02047': 'Stahlberg Felix',
  '1611-07053': 'Grozdanov Sašo, Starinets Andrei O.',
  '1711-07982': 'Williamson Dominic J., Bultinck Nick, Verstraete Frank',
  '1604-05544': 'Caselle Michele, Costagliola Gianluca, Nada Alessandro, Panero Marco, Toniato Arianna',
  '1908-09858': 'Cherman Aleksey, Jacobson Theodore, Tanizaki Yuya, Ünsal Mithat',
  '1610-03911': 'Wen Xiao-Gang',
  '1210-054': 'Kim Bom Soo',
  '1912-08957': 'Sun Ruoyu',
  '1912-01006': 'Dedushenko Mykola, Wang Yifan',
  '1608-05351': 'Awata Hidetoshi, Kanno Hiroaki, Mironov Andrei, Morozov Alexei, Morozov Andrey, Ohkubo Yusuke, Zenkevich Yegor',
  '1810-01185': 'Serban Alexandru Constantin, Poll Erik, Visser Joost',
  '1801-08156': 'Pisarski Robert D., Skokov Vladimir V., Tsvelik Alexei M.',
  '1211-1273': 'Reshetnyak Alexander A.',
  '1603-08382': 'Bullimore Mathew, Dimofte Tudor, Gaiotto Davide, Hilburn Justin',
  '2002-05442': 'Le Triet H. M., Chen Hao, Babar M. Ali',
  '1801-00553': 'Akhtar Naveed, Mian Ajmal',
  '1808-09434': 'Klebanov Igor R., Popov Fedor, Tarnopolsky Grigory',
  '1807-08169': 'Minar Matiur Rahman, Naher Jibon',
  '1809-03193': 'Agarwal Shivang, Terrail Jean Ogier Du, Jurie Frédéric',
  '1410-6201': 'Buchel Alex, Myers Robert C., van Niekerk Anton',
  '1802-09439': 'Dittrich Bianca',
  '1910-10045': 'Arrieta Alejandro Barredo, Díaz-Rodríguez Natalia, Del Ser Javier, Bennetot Adrien, Tabik Siham, Barbado Alberto, García Salvador, Gil-López Sergio, Molina Daniel, Benjamins Richard, Chatila Raja, Herrera Francisco',
  '1706-04054': 'Li Wenliang',
  '1808-09072': 'Takayanagi Tadashi',
  '1904-02704': 'Dedushenko Mykola, Fluder Martin',
  '1110-5044': 'Buchbinder I. L., Reshetnyak A.',
  '1401-7788': 'Gattringer Christof',
  '1809-07294': 'Yi Xin, Walia Ekta, Babyn Paul',
  '1910-03584': 'Else Dominic V., Ho Wen Wei, Dumitrescu Philipp T.',
  '1911-05741': 'Dedushenko Mykola',
  '1801-05416': 'Wang Juven, Ohmori Kantaro, Putrov Pavel, Zheng Yunqin, Wan Zheyan, Guo Meng, Lin Hai, Gao Peng, Yau Shing-Tung',
  '1807-11939': 'Wilde Mark M.',
  '1810-05165': 'Komiske Patrick T., Metodiev Eric M., Thaler Jesse',
  '1912-03324': 'Chester Shai M., Landry Walter, Liu Junyu, Poland David, Simmons-Duffin David, Su Ning, Vichi Alessandro',
  '1902-09166': 'Hongo Masaru, Hidaka Yoshimasa',
  '1603-0877': 'Grozdanov Sašo, Poovuttikul Napat',
  '1905-02191': 'Kusuki Yuya, Miyaji Masamichi',
  '1910-03883': 'Khatri Sumeet, Kaur Eneet, Guha Saikat, Wilde Mark M.',
  '1611-07304': 'Awata H., Kanno H., Mironov A., Morozov A., Morozov An., Ohkubo Y., Zenkevich Y.',
  '1706-03044': 'Kanazawa Takuya, Wettig Tilo',
  '1303-2287': 'Hasebe Kazuki, Totsuka Keisuke',
  '1301-198': 'Pasukonis Jurgis, Ramgoolam Sanjaye',
  '1809-00736': 'Nieri Fabrizio, Pan Yiwen, Zabzine Maxim',
  '1202-6062': 'Kim Bom Soo'},
 'year': {'1004-3169': 2010,
  '1612-07324': 2018,
  '1101-0618': 2012,
  '1712-03107': 2018,
  '801-2826': 2011,
  '1503-00732': 2015,
  '1805-04405': 2019,
  '1712-05815': 2019,
  '1302-028': 2013,
  '1106-1445': 2019,
  '1909-11512': 2019,
  '1204-245': 2012,
  '1302-0884': 2014,
  '1804-06469': 2018,
  '1812-02893': 2020,
  '1903-05082': 2019,
  '1610-08526': 2018,
  '1711-00394': 2018,
  '1003-1366': 2012,
  '1104-3712': 2011,
  '1710-08425': 2018,
  '1410-8712': 2015,
  '1003-4725': 2010,
  '1903-10563': 2019,
  '1805-06467': 2019,
  '1912-06855': 2019,
  '1901-05895': 2019,
  '1511-04265': 2016,
  '1606-08953': 2016,
  '1807-03334': 2018,
  '905-0932': 2009,
  '1409-1178': 2014,
  '1909-02005': 2019,
  '2002-12187': 2021,
  '905-4013': 2009,
  '1803-08823': 2019,
  '1803-01164': 2018,
  '1908-02667': 2019,
  '2001-06937': 2020,
  '1910-04713': 2023,
  '1603-09741': 2016,
  '1409-3575': 2016,
  '1805-12137': 2018,
  '1903-00491': 2019,
  '1912-04977': 2021,
  '1905-10378': 2019,
  '1811-1256': 2018,
  '1907-04332': 2019,
  '1908-00013': 2020,
  '1903-06633': 2019,
  '1110-3814': 2011,
  '1311-7565': 2014,
  '806-3474': 2009,
  '1312-6689': 2013,
  '1712-08016': 2018,
  '1901-07038': 2019,
  '1912-02047': 2020,
  '1611-07053': 2017,
  '1711-07982': 2017,
  '1604-05544': 2016,
  '1908-09858': 2020,
  '1610-03911': 2017,
  '1210-054': 2012,
  '1912-08957': 2019,
  '1912-01006': 2019,
  '1608-05351': 2016,
  '1810-01185': 2019,
  '1801-08156': 2018,
  '1211-1273': 2018,
  '1603-08382': 2016,
  '2002-05442': 2020,
  '1801-00553': 2018,
  '1808-09434': 2018,
  '1807-08169': 2018,
  '1809-03193': 2019,
  '1410-6201': 2015,
  '1802-09439': 2018,
  '1910-10045': 2019,
  '1706-04054': 2018,
  '1808-09072': 2018,
  '1904-02704': 2019,
  '1110-5044': 2012,
  '1401-7788': 2014,
  '1809-07294': 2019,
  '1910-03584': 2020,
  '1911-05741': 2021,
  '1801-05416': 2018,
  '1807-11939': 2018,
  '1810-05165': 2019,
  '1912-03324': 2020,
  '1902-09166': 2019,
  '1603-0877': 2016,
  '1905-02191': 2019,
  '1910-03883': 2021,
  '1611-07304': 2017,
  '1706-03044': 2017,
  '1303-2287': 2013,
  '1301-198': 2013,
  '1809-00736': 2018,
  '1202-6062': 2012},
 '# citations': {'1004-3169': 1266,
  '1612-07324': 626,
  '1101-0618': 568,
  '1712-03107': 534,
  '801-2826': 505,
  '1503-00732': 492,
  '1805-04405': 421,
  '1712-05815': 368,
  '1302-028': 268,
  '1106-1445': 257,
  '1909-11512': 229,
  '1204-245': 222,
  '1302-0884': 218,
  '1804-06469': 208,
  '1812-02893': 201,
  '1903-05082': 197,
  '1610-08526': 194,
  '1711-00394': 186,
  '1003-1366': 185,
  '1104-3712': 184,
  '1710-08425': 180,
  '1410-8712': 180,
  '1003-4725': 177,
  '1903-10563': 176,
  '1805-06467': 173,
  '1912-06855': 172,
  '1901-05895': 172,
  '1511-04265': 164,
  '1606-08953': 162,
  '1807-03334': 159,
  '905-0932': 158,
  '1409-1178': 158,
  '1909-02005': 153,
  '2002-12187': 153,
  '905-4013': 146,
  '1803-08823': 144,
  '1803-01164': 143,
  '1908-02667': 143,
  '2001-06937': 142,
  '1910-04713': 140,
  '1603-09741': 137,
  '1409-3575': 137,
  '1805-12137': 135,
  '1903-00491': 134,
  '1912-04977': 133,
  '1905-10378': 132,
  '1811-1256': 131,
  '1907-04332': 131,
  '1908-00013': 130,
  '1903-06633': 130,
  '1110-3814': 130,
  '1311-7565': 128,
  '806-3474': 127,
  '1312-6689': 127,
  '1712-08016': 127,
  '1901-07038': 127,
  '1912-02047': 126,
  '1611-07053': 126,
  '1711-07982': 126,
  '1604-05544': 125,
  '1908-09858': 124,
  '1610-03911': 121,
  '1210-054': 121,
  '1912-08957': 121,
  '1912-01006': 120,
  '1608-05351': 120,
  '1810-01185': 120,
  '1801-08156': 119,
  '1211-1273': 117,
  '1603-08382': 117,
  '2002-05442': 117,
  '1801-00553': 115,
  '1808-09434': 114,
  '1807-08169': 113,
  '1809-03193': 112,
  '1410-6201': 112,
  '1802-09439': 111,
  '1910-10045': 111,
  '1706-04054': 111,
  '1808-09072': 111,
  '1904-02704': 110,
  '1110-5044': 109,
  '1401-7788': 108,
  '1809-07294': 108,
  '1910-03584': 107,
  '1911-05741': 107,
  '1801-05416': 106,
  '1807-11939': 105,
  '1810-05165': 105,
  '1912-03324': 105,
  '1902-09166': 104,
  '1603-0877': 104,
  '1905-02191': 104,
  '1910-03883': 104,
  '1611-07304': 104,
  '1706-03044': 103,
  '1303-2287': 103,
  '1301-198': 103,
  '1809-00736': 103,
  '1202-6062': 103}}

categories_list={'group_name': {0: 'Computer Science',
  3: 'Computer Science',
  4: 'Computer Science',
  5: 'Computer Science',
  6: 'Computer Science',
  7: 'Computer Science',
  8: 'Computer Science',
  9: 'Computer Science',
  10: 'Computer Science',
  11: 'Computer Science',
  12: 'Computer Science',
  13: 'Computer Science',
  14: 'Computer Science',
  15: 'Computer Science',
  16: 'Computer Science',
  18: 'Computer Science',
  19: 'Computer Science',
  20: 'Computer Science',
  21: 'Computer Science',
  22: 'Computer Science',
  23: 'Computer Science',
  24: 'Computer Science',
  26: 'Computer Science',
  27: 'Computer Science',
  28: 'Computer Science',
  29: 'Computer Science',
  34: 'Computer Science',
  38: 'Computer Science',
  40: 'Economics',
  43: 'Electrical Engineering and Systems Science',
  44: 'Electrical Engineering and Systems Science',
  45: 'Electrical Engineering and Systems Science',
  51: 'Mathematics',
  53: 'Mathematics',
  56: 'Mathematics',
  57: 'Mathematics',
  59: 'Mathematics',
  68: 'Mathematics',
  71: 'Mathematics',
  72: 'Mathematics',
  75: 'Mathematics',
  78: 'Mathematics',
  85: 'Physics',
  91: 'Physics',
  92: 'Physics',
  100: 'Physics',
  101: 'Physics',
  149: 'Statistics',
  150: 'Statistics',
  151: 'Statistics',
  152: 'Statistics',
  153: 'Statistics',
  154: 'Statistics'},
 'category_name': {0: 'Artificial Intelligence',
  3: 'Computational Engineering, Finance, and Science',
  4: 'Computational Geometry',
  5: 'Computation and Language',
  6: 'Cryptography and Security',
  7: 'Computer Vision and Pattern Recognition',
  8: 'Computers and Society',
  9: 'Databases',
  10: 'Distributed, Parallel, and Cluster Computing',
  11: 'Digital Libraries',
  12: 'Discrete Mathematics',
  13: 'Data Structures and Algorithms',
  14: 'Emerging Technologies',
  15: 'Formal Languages and Automata Theory',
  16: 'General Literature',
  18: 'Computer Science and Game Theory',
  19: 'Human-Computer Interaction',
  20: 'Information Retrieval',
  21: 'Information Theory',
  22: 'Machine Learning',
  23: 'Logic in Computer Science',
  24: 'Multiagent Systems',
  26: 'Mathematical Software',
  27: 'Numerical Analysis',
  28: 'Neural and Evolutionary Computing',
  29: 'Networking and Internet Architecture',
  34: 'Robotics',
  38: 'Social and Information Networks',
  40: 'Econometrics',
  43: 'Audio and Speech Processing',
  44: 'Image and Video Processing',
  45: 'Signal Processing',
  51: 'Classical Analysis and ODEs',
  53: 'Category Theory',
  56: 'Dynamical Systems',
  57: 'Functional Analysis',
  59: 'General Topology',
  68: 'Numerical Analysis',
  71: 'Optimization and Control',
  72: 'Probability',
  75: 'Representation Theory',
  78: 'Statistics Theory',
  85: 'Disordered Systems and Neural Networks',
  91: 'Statistical Mechanics',
  92: 'Strongly Correlated Electrons',
  100: 'Adaptation and Self-Organizing Systems',
  101: 'Chaotic Dynamics',
  149: 'Applications',
  150: 'Computation',
  151: 'Methodology',
  152: 'Machine Learning',
  153: 'Other Statistics',
  154: 'Statistics Theory'},
 'category_id': {0: 'cs.AI',
  3: 'cs.CE',
  4: 'cs.CG',
  5: 'cs.CL',
  6: 'cs.CR',
  7: 'cs.CV',
  8: 'cs.CY',
  9: 'cs.DB',
  10: 'cs.DC',
  11: 'cs.DL',
  12: 'cs.DM',
  13: 'cs.DS',
  14: 'cs.ET',
  15: 'cs.FL',
  16: 'cs.GL',
  18: 'cs.GT',
  19: 'cs.HC',
  20: 'cs.IR',
  21: 'cs.IT',
  22: 'cs.LG',
  23: 'cs.LO',
  24: 'cs.MA',
  26: 'cs.MS',
  27: 'cs.NA',
  28: 'cs.NE',
  29: 'cs.NI',
  34: 'cs.RO',
  38: 'cs.SI',
  40: 'econ.EM',
  43: 'eess.AS',
  44: 'eess.IV',
  45: 'eess.SP',
  51: 'math.CA',
  53: 'math.CT',
  56: 'math.DS',
  57: 'math.FA',
  59: 'math.GN',
  68: 'math.NA',
  71: 'math.OC',
  72: 'math.PR',
  75: 'math.RT',
  78: 'math.ST',
  85: 'cond-mat.dis-nn',
  91: 'cond-mat.stat-mech',
  92: 'cond-mat.str-el',
  100: 'nlin.AO',
  101: 'nlin.CD',
  149: 'stat.AP',
  150: 'stat.CO',
  151: 'stat.ME',
  152: 'stat.ML',
  153: 'stat.OT',
  154: 'stat.TH'},
 'category_description': {0: 'Covers all areas of AI except Vision, Robotics, Machine Learning, Multiagent Systems, and Computation and Language (Natural Language Processing), which have separate subject areas. In particular, includes Expert Systems, Theorem Proving (although this may overlap with Logic in Computer Science), Knowledge Representation, Planning, and Uncertainty in AI. Roughly includes material in ACM Subject Classes I.2.0, I.2.1, I.2.3, I.2.4, I.2.8, and I.2.11.',
  3: 'Covers applications of computer science to the mathematical modeling of complex systems in the fields of science, engineering, and finance. Papers here are interdisciplinary and applications-oriented, focusing on techniques and tools that enable challenging computational simulations to be performed, for which the use of supercomputers or distributed computing platforms is often required. Includes material in ACM Subject Classes J.2, J.3, and J.4 (economics).',
  4: 'Roughly includes material in ACM Subject Classes I.3.5 and F.2.2.',
  5: 'Covers natural language processing. Roughly includes material in ACM Subject Class I.2.7. Note that work on artificial languages (programming languages, logics, formal systems) that does not explicitly address natural-language issues broadly construed (natural-language processing, computational linguistics, speech, text retrieval, etc.) is not appropriate for this area.',
  6: 'Covers all areas of cryptography and security including authentication, public key cryptosytems, proof-carrying code, etc. Roughly includes material in ACM Subject Classes D.4.6 and E.3.',
  7: 'Covers image processing, computer vision, pattern recognition, and scene understanding. Roughly includes material in ACM Subject Classes I.2.10, I.4, and I.5.',
  8: 'Covers impact of computers on society, computer ethics, information technology and public policy, legal aspects of computing, computers and education. Roughly includes material in ACM Subject Classes K.0, K.2, K.3, K.4, K.5, and K.7.',
  9: 'Covers database management, datamining, and data processing. Roughly includes material in ACM Subject Classes E.2, E.5, H.0, H.2, and J.1.',
  10: 'Covers fault-tolerance, distributed algorithms, stabilility, parallel computation, and cluster computing. Roughly includes material in ACM Subject Classes C.1.2, C.1.4, C.2.4, D.1.3, D.4.5, D.4.7, E.1.',
  11: 'Covers all aspects of the digital library design and document and text creation. Note that there will be some overlap with Information Retrieval (which is a separate subject area). Roughly includes material in ACM Subject Classes H.3.5, H.3.6, H.3.7, I.7.',
  12: 'Covers combinatorics, graph theory, applications of probability. Roughly includes material in ACM Subject Classes G.2 and G.3.',
  13: 'Covers data structures and analysis of algorithms. Roughly includes material in ACM Subject Classes E.1, E.2, F.2.1, and F.2.2.',
  14: 'Covers approaches to information processing (computing, communication, sensing) and bio-chemical analysis based on alternatives to silicon CMOS-based technologies, such as nanoscale electronic, photonic, spin-based, superconducting, mechanical, bio-chemical and quantum technologies (this list is not exclusive). Topics of interest include (1) building blocks for emerging technologies, their scalability and adoption in larger systems, including integration with traditional technologies, (2) modeling, design and optimization of novel devices and systems, (3) models of computation, algorithm design and programming for emerging technologies.',
  15: 'Covers automata theory, formal language theory, grammars, and combinatorics on words. This roughly corresponds to ACM Subject Classes F.1.1, and F.4.3. Papers dealing with computational complexity should go to cs.CC; papers dealing with logic should go to cs.LO.',
  16: 'Covers introductory material, survey material, predictions of future trends, biographies, and miscellaneous computer-science related material. Roughly includes all of ACM Subject Class A, except it does not include conference proceedings (which will be listed in the appropriate subject area).',
  18: 'Covers all theoretical and applied aspects at the intersection of computer science and game theory, including work in mechanism design, learning in games (which may overlap with Learning), foundations of agent modeling in games (which may overlap with Multiagent systems), coordination, specification and formal methods for non-cooperative computational environments. The area also deals with applications of game theory to areas such as electronic commerce.',
  19: 'Covers human factors, user interfaces, and collaborative computing. Roughly includes material in ACM Subject Classes H.1.2 and all of H.5, except for H.5.1, which is more likely to have Multimedia as the primary subject area.',
  20: 'Covers indexing, dictionaries, retrieval, content and analysis. Roughly includes material in ACM Subject Classes H.3.0, H.3.1, H.3.2, H.3.3, and H.3.4.',
  21: 'Covers theoretical and experimental aspects of information theory and coding. Includes material in ACM Subject Class E.4 and intersects with H.1.1.',
  22: 'Papers on all aspects of machine learning research (supervised, unsupervised, reinforcement learning, bandit problems, and so on) including also robustness, explanation, fairness, and methodology. cs.LG is also an appropriate primary category for applications of machine learning methods.',
  23: 'Covers all aspects of logic in computer science, including finite model theory, logics of programs, modal logic, and program verification. Programming language semantics should have Programming Languages as the primary subject area. Roughly includes material in ACM Subject Classes D.2.4, F.3.1, F.4.0, F.4.1, and F.4.2; some material in F.4.3 (formal languages) may also be appropriate here, although Computational Complexity is typically the more appropriate subject area.',
  24: 'Covers multiagent systems, distributed artificial intelligence, intelligent agents, coordinated interactions. and practical applications. Roughly covers ACM Subject Class I.2.11.',
  26: 'Roughly includes material in ACM Subject Class G.4.',
  27: 'cs.NA is an alias for math.NA. Roughly includes material in ACM Subject Class G.1.',
  28: 'Covers neural networks, connectionism, genetic algorithms, artificial life, adaptive behavior. Roughly includes some material in ACM Subject Class C.1.3, I.2.6, I.5.',
  29: 'Covers all aspects of computer communication networks, including network architecture and design, network protocols, and internetwork standards (like TCP/IP). Also includes topics, such as web caching, that are directly relevant to Internet architecture and performance. Roughly includes all of ACM Subject Class C.2 except C.2.4, which is more likely to have Distributed, Parallel, and Cluster Computing as the primary subject area.',
  34: 'Roughly includes material in ACM Subject Class I.2.9.',
  38: 'Covers the design, analysis, and modeling of social and information networks, including their applications for on-line information access, communication, and interaction, and their roles as datasets in the exploration of questions in these and other domains, including connections to the social and biological sciences. Analysis and modeling of such networks includes topics in ACM Subject classes F.2, G.2, G.3, H.2, and I.2; applications in computing include topics in H.3, H.4, and H.5; and applications at the interface of computing and other disciplines include topics in J.1--J.7. Papers on computer communication systems and network protocols (e.g. TCP/IP) are generally a closer fit to the Networking and Internet Architecture (cs.NI) category.',
  40: 'Econometric Theory, Micro-Econometrics, Macro-Econometrics, Empirical Content of Economic Relations discovered via New Methods, Methodological Aspects of the Application of Statistical Inference to Economic Data.',
  43: 'Theory and methods for processing signals representing audio, speech, and language, and their applications. This includes analysis, synthesis, enhancement, transformation, classification and interpretation of such signals as well as the design, development, and evaluation of associated signal processing systems. Machine learning and pattern analysis applied to any of the above areas is also welcome.  Specific topics of interest include: auditory modeling and hearing aids; acoustic beamforming and source localization; classification of acoustic scenes; speaker separation; active noise control and echo cancellation; enhancement; de-reverberation; bioacoustics; music signals analysis, synthesis and modification; music information retrieval;  audio for multimedia and joint audio-video processing; spoken and written language modeling, segmentation, tagging, parsing, understanding, and translation; text mining; speech production, perception, and psychoacoustics; speech analysis, synthesis, and perceptual modeling and coding; robust speech recognition; speaker recognition and characterization; deep learning, online learning, and graphical models applied to speech, audio, and language signals; and implementation aspects ranging from system architecture to fast algorithms.',
  44: 'Theory, algorithms, and architectures for the formation, capture, processing, communication, analysis, and display of images, video, and multidimensional signals in a wide variety of applications. Topics of interest include: mathematical, statistical, and perceptual image and video modeling and representation; linear and nonlinear filtering, de-blurring, enhancement, restoration, and reconstruction from degraded, low-resolution or tomographic data; lossless and lossy compression and coding; segmentation, alignment, and recognition; image rendering, visualization, and printing; computational imaging, including ultrasound, tomographic and magnetic resonance imaging; and image and video analysis, synthesis, storage, search and retrieval.',
  45: 'Theory, algorithms, performance analysis and applications of signal and data analysis, including physical modeling, processing, detection and parameter estimation, learning, mining, retrieval, and information extraction. The term "signal" includes speech, audio, sonar, radar, geophysical, physiological, (bio-) medical, image, video, and multimodal natural and man-made signals, including communication signals and data. Topics of interest include: statistical signal processing, spectral estimation and system identification; filter design, adaptive filtering / stochastic learning; (compressive) sampling, sensing, and transform-domain methods including fast algorithms; signal processing for machine learning and machine learning for signal processing applications; in-network and graph signal processing; convex and nonconvex optimization methods for signal processing applications; radar, sonar, and sensor array beamforming and direction finding; communications signal processing; low power, multi-core and system-on-chip signal processing; sensing, communication, analysis and optimization for cyber-physical systems such as power grids and the Internet of Things.',
  51: "Special functions, orthogonal polynomials, harmonic analysis, ODE's, differential relations, calculus of variations, approximations, expansions, asymptotics",
  53: 'Enriched categories, topoi, abelian categories, monoidal categories, homological algebra',
  56: 'Dynamics of differential equations and flows, mechanics, classical few-body problems, iterations, complex dynamics, delayed differential equations',
  57: 'Banach spaces, function spaces, real functions, integral transforms, theory of distributions, measure theory',
  59: 'Continuum theory, point-set topology, spaces with algebraic structure, foundations, dimension theory, local and global properties',
  68: 'Numerical algorithms for problems in analysis and algebra, scientific computation',
  71: 'Operations research, linear programming, control theory, systems theory, optimal control, game theory',
  72: 'Theory and applications of probability and stochastic processes: e.g. central limit theorems, large deviations, stochastic differential equations, models from statistical mechanics, queuing theory',
  75: 'Linear representations of algebras and groups, Lie theory, associative algebras, multilinear algebra',
  78: 'Applied, computational and theoretical statistics: e.g. statistical inference, regression, time series, multivariate analysis, data analysis, Markov chain Monte Carlo, design of experiments, case studies',
  85: 'Glasses and spin glasses; properties of random, aperiodic and quasiperiodic systems; transport in disordered media; localization; phenomena mediated by defects and disorder; neural networks',
  91: 'Phase transitions, thermodynamics, field theory, non-equilibrium phenomena, renormalization group and scaling, integrable models, turbulence',
  92: 'Quantum magnetism, non-Fermi liquids, spin liquids, quantum criticality, charge density waves, metal-insulator transitions',
  100: 'Adaptation, self-organizing systems, statistical physics, fluctuating systems, stochastic processes, interacting particle systems, machine learning',
  101: 'Dynamical systems, chaos, quantum chaos, topological dynamics, cycle expansions, turbulence, propagation',
  149: 'Biology, Education, Epidemiology, Engineering, Environmental Sciences, Medical, Physical Sciences, Quality Control, Social Sciences',
  150: 'Algorithms, Simulation, Visualization',
  151: 'Design, Surveys, Model Selection, Multiple Testing, Multivariate Methods, Signal and Image Processing, Time Series, Smoothing, Spatial Statistics, Survival Analysis, Nonparametric and Semiparametric Methods',
  152: 'Covers machine learning papers (supervised, unsupervised, semi-supervised learning, graphical models, reinforcement learning, bandits, high dimensional inference, etc.) with a statistical or theoretical grounding',
  153: 'Work in statistics that does not fit into the other stat classifications',
  154: 'stat.TH is an alias for math.ST. Asymptotics, Bayesian Inference, Decision Theory, Estimation, Foundations, Inference, Testing.'}}

st.markdown("<h3 style='text-align: center; color: #289c68'>🧩 Rᴇsᴇᴀʀcʜ Puʟsᴇ 🧩</h3>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #a62c19'> ﮩ٨ـﮩﮩ٨ـﮩ٨ـﮩـ</h4>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align: center; color: grey;'>NLP-powered assistive exploration of research papers in AI / ML related fields</h6>", unsafe_allow_html=True)

Dashboard, Search, Papers, Authors, Tools, About = st.tabs(["-Dashboard-","-Search-","-Research Papers-","-Research Authors-","-Tools-","-About-"])

with Dashboard:
    Aggregates, Rankings, Categories = Dashboard.tabs(["Aggregates","Rankings","by Category (soon)"])
    with Aggregates:
        st.markdown("  ")
        st.markdown("<h6 style='text-align: center; color: #289c68'>All categories available</h6>", unsafe_allow_html=True)
        st.write(pd.DataFrame(categories_list).set_index('group_name'))
        st.markdown("---")
        st.markdown("  ")
        st.markdown("<h6 style='text-align: center; color: #289c68'>Aggregate number of papers per year</h6>", unsafe_allow_html=True)
        st.image('https://storage.googleapis.com/deepdipper_data/images/aggregate/agg_number_papers_year.png', caption='Number of papers per year', use_column_width=True)
        st.markdown("---")
        st.markdown("  ")
        st.markdown("<h6 style='text-align: center; color: #289c68'>Aggregate number of papers & citations per year</h6>", unsafe_allow_html=True)
        st.image('https://storage.googleapis.com/deepdipper_data/images/aggregate/agg_number_public_citations.png', caption='Number of papers and citations per year', use_column_width=True)
        st.markdown("  ")

    with Rankings:
        st.markdown("  ")
        st.markdown("<h6 style='text-align: center; color: #289c68'>Top 100 most cited papers</h6>", unsafe_allow_html=True)
        st.write(pd.DataFrame(top100_papers))
        st.markdown("---")
        st.markdown("  ")
        col1, col2= st.columns(2)
        with col1:
            st.markdown("<h6 style='text-align: center; color: #289c68'>Top 20 categories with most papers</h6>", unsafe_allow_html=True)
            st.image('https://storage.googleapis.com/deepdipper_data/images/ranking/top_20_categories.png', caption='Categories with most publications', use_column_width=True)
        with col2:
            st.markdown("<h6 style='text-align: center; color: #289c68'>Top 30 words in all papers</h6>", unsafe_allow_html=True)
            st.image('https://storage.googleapis.com/deepdipper_data/images/ranking/top30_wordcloud.png', caption='Most frequent technical words', use_column_width=True)
        st.markdown("---")
        st.markdown("  ")
        st.markdown("<h6 style='text-align: center; color: #289c68'>Top 30 most cited authors</h6>", unsafe_allow_html=True)
        st.image('https://storage.googleapis.com/deepdipper_data/images/ranking/top_30_authors_cited.png', caption='Ranked authors by citations', use_column_width=True)

    with Categories:
        st.text(' ')
        st.markdown('-- coming soon, stay tuned! --')

with Search:

    Search_Papers_Keywords,Search_Papers_Authors,Search_Authors = Search.tabs(["Papers by keyword(s)","Papers by author name","Authors by name (soon)"])

    with Search_Papers_Keywords:
        result_type1 = st.radio("Type of search : ",("Similarity (default)", "Most recent", "Most cited"),)
        with st.form(key='params_for_api_search_papers') as search_form:
            input1 = st.text_input('\> input one to five keywords separated by space, at least related by far to artifical intelligence and machine learning')
            if st.form_submit_button('Search for Papers !'):
                if result_type1 == "Most recent":
                    result_type1 = 'most_recent'
                elif result_type1 == "Most cited":
                    result_type1 = 'most_cited'
                else:
                    result_type1 = 'default'
                params1 = input1.replace(' ','-').lower()

                # deepdipper_api_url1 = 'http://127.0.0.1:8000/search'
                deepdipper_api_url1 = 'https://deepdipper-rp6v7d7m4q-ew.a.run.app/search'

                with st.spinner("Calculating cosine similarity between your input and all available papers' abstracts..."):
                    #response1 = requests.get(deepdipper_api_url1+params1)
                    response1 = requests.get(deepdipper_api_url1, params=dict(query=params1,result_type=result_type1))

                results1 = response1.json()
                st.markdown(' ')

                #st.header('Top result:')
                st.markdown(' ')
                st.markdown(f"<h5 style='text-align: center; color: #289c68'>Top 50 papers ({result_type1.replace('_',' ')})</h5>", unsafe_allow_html=True)
                st.markdown(' ')
                st.markdown(' ')
                for i in range(0,50):
                    k=f'{i}'
                    st.markdown(f"<h6 style='text-align: center; color: #289c68'>#{i+1} -- {str(results1[k]['Title'])}</h6>", unsafe_allow_html=True)
                    st.markdown(str(results1[k]['Year'])+ ', ' + str(results1[k]['Authors']) + ', ' + results1[k]['Link'])
                    st.markdown('Cited ' + str(results1[k]['Number_citations']) + ' times -- Paper ID: ' + str(results1[k]['Id'])+ ' -- Category: ' + str(results1[k]['Category']))
                    st.text('ABSTRACT -- ' + results1[k]['Abstract'])
                    st.text(' ')
                    st.markdown("---")
                    st.text(' ')

    with Search_Papers_Authors:
        with st.form(key='params_for_api_search_authors'):

            input2 = st.text_input('\> input name to get all papers from authors containing this name')

            if st.form_submit_button('Search for Authors !'):

                params2 = input2.replace(' ','-').lower()

                #deepdipper_api_url2 = 'http://127.0.0.1:8000/authors?query='
                deepdipper_api_url2 = 'https://deepdipper-rp6v7d7m4q-ew.a.run.app/authors'

                with st.spinner('Finding papers...'):
                    #response2 = requests.get(deepdipper_api_url2+params2)
                    response2 = requests.get(deepdipper_api_url2, params=dict(query=params2))

                results2 = response2.json()

                for key in results2:
                    st.markdown(f"<h6 style='text-align: center; color: #289c68'>---  {str(results2[key]['Title'])}  ---</h6>", unsafe_allow_html=True)
                    st.markdown(str(results2[key]['Year'])+ ', ' + str(results2[key]['Authors']) + ', ' + str(results2[key]['Link']))
                    st.markdown('Cited ' + str(results2[key]['Number_citations']) + ' times -- Paper ID: ' + str(results2[key]['Id'])+ ' -- Category: ' + str(results2[key]['Category']))
                    st.text('ABSTRACT -- ' + str(results2[key]['Abstract']))
                    st.text(' ')
                    st.markdown(' --- ')
                    st.text(' ')

    with Search_Authors:
        st.text(' ')
        st.markdown('-- coming soon, stay tuned! --')

with Papers:
    with st.form(key='params_for_api_research_paper'):

        input3 = st.text_input('\> input exact paper ID to get detailed info on it (e.g. 1606-01781, 1706-03059, 1903-06236...)')

        if st.form_submit_button('Research Paper !'):

            params3 = input3.replace(' ','-').lower()

            #deepdipper_api_url3 = 'http://127.0.0.1:8000/papers?query='
            deepdipper_api_url3 = 'https://deepdipper-rp6v7d7m4q-ew.a.run.app/papers'

            with st.spinner('Looking for Paper details...'):
                response3 = requests.get(deepdipper_api_url3, params=dict(query=params3))

            results3 = response3.json()

            st.text(' ')
            for key in results3:
                st.markdown(f"<h6 style='text-align: center; color: #289c68'>--- {str(results3[key]['Title'])} ---</h6>", unsafe_allow_html=True)
                st.markdown('By : ' + str(results3[key]['Authors']))
                st.markdown('Cited ' + str(results3[key]['Number_citations']) + ' times -- Published in ' + str(results3[key]['Year']))
                st.markdown('arXiv category : ' + str(results3[key]['Category']) + ' -- Paper ID : ' + str(results3[key]['Id']))

                st.text(' ')


            #deepdipper_api_url6 = 'http://127.0.0.1:8000/citations?query='
            deepdipper_api_url6 = 'https://deepdipper-rp6v7d7m4q-ew.a.run.app/citations'

            with st.spinner('Looking for papers citing this one...'):
                response6 = requests.get(deepdipper_api_url6, params=dict(query=params3))

            results6 = response6.json()

            df6 = pd.DataFrame.from_dict(results6, orient='index', columns=['Title', 'Authors', 'Id', 'Year', 'Link', 'Category', 'Number_citations', 'Abstract'])[['Id', 'Category', 'Year', 'Title', 'Number_citations', 'Authors']]
            df6['Year'] = df6['Year'].astype(int)
            df6.sort_values(by=['Year'], inplace=True,ascending=False)
            df6['Year'] = df6['Year'].astype(str)
            st.markdown(' --- ')
            st.markdown(f"<h6 style='text-align: center; color: #289c68'> All papers citing paper_id {params3} :</h6>", unsafe_allow_html=True)

            st.write(df6.set_index('Id'))

            st.text(' ')
            st.markdown('---')
            st.text(' ')

            st.text('below not rendering yet on major browsers... :(')

            for key in results3:
                arxiv_url=results3[key]['Link']
                pdf_url = F'http://docs.google.com/gview?url={arxiv_url}&embedded=true'
                st.markdown(pdf_url, unsafe_allow_html=True)
                http = urllib3.PoolManager()
                response = http.request('GET', arxiv_url)
                remoteFile = response.data


                response2 = requests.get(arxiv_url)

                if response2.status_code == 200:
                    # If the request is successful, encode the PDF content as base64 data
                    pdf_data = b64encode(response2.content).decode('utf-8')

                    # Display the PDF using an iframe
                    st.markdown(f'<iframe src="data:application/pdf;base64,{pdf_data}" width="700" height="1000"></iframe>', unsafe_allow_html=True)

                else:
                    st.markdown("Error loading PDF")

                # # Convert the PDF data to an image
                # pdf_pages = convert_from_bytes(remoteFile, dpi=200)
                # pdf_image = pdf_pages[0]  # Select the first page of the PDF

                # # Render the PDF image in Streamlit
                # st.image(pdf_image)

                # Convert the PDF data to base64 format
                pdf_data = BytesIO(remoteFile)
                b64_pdf = b64encode(pdf_data.read()).decode('utf-8')

                # Render the PDF in Streamlit
                pdf_display = f'<embed src="data:application/pdf;base64,{b64_pdf}" width="700" height="1000" type="application/pdf">'
                st.markdown(pdf_display, unsafe_allow_html=True)

                # response_pdf = requests.get(pdf_url)
                # pdf_data = BytesIO(response_pdf.content)
                # base64_pdf = b64encode(pdf_data.read()).decode('utf-8')

                # images = pdf2image.convert_from_bytes(pdf_data.read())
                # for i in range(len(images)):
                #     st.image(images[i], caption=f'pdf page {i}', use_column_width=True)

                # pdf_viewer = f'<iframe src="{pdf_url}" width="600" height="800"></iframe>'
                # st.markdown(pdf_viewer, unsafe_allow_html=True)
                # with open(pdf_url, 'rb') as f:
                #     base64_pdf = b64encode(f.read()).decode('utf-8')

                # pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="600" height="800" type="application/pdf"></iframe>'

                # pdf_display = F'<iframe src="{pdf_url}" width="700" height="900" type="application/pdf"></iframe>'
                # st.markdown(pdf_display, unsafe_allow_html=True)
                # # st.markdown(pdf_display, unsafe_allow_html=True)
                # response_pdf = requests.get(pdf_url)

                # # Read the downloaded binary data into a BytesIO object
                # pdf_data = BytesIO(response_pdf.content)
                # # Generate the HTML code to display the PDF
                # base64_pdf = b64encode(pdf_data.read()).decode('utf-8')
                # # Display the PDF
                # st.markdown(f'<embed src="data:application/pdf;base64,{base64_pdf}" width="600" height="800" type="application/pdf">', unsafe_allow_html=True)

with Authors:
    with st.form(key='params_for_api_research_author'):

        input4 = st.text_input('\> input exact author name to get detailed info on them (family then first name e.g. Chollet Francois, Lecun Yann..)')

        if st.form_submit_button('Research Author !'):

            params4 = input4.replace(' ','-').lower()

            #deepdipper_api_url4 = 'http://127.0.0.1:8000/authors?query='
            deepdipper_api_url4 = 'https://deepdipper-rp6v7d7m4q-ew.a.run.app/authors'

            with st.spinner('Looking for Author details...'):
                #response4 = requests.get(deepdipper_api_url4+params4)
                response4 = requests.get(deepdipper_api_url4, params=dict(query=params4))
                results4 = response4.json()
                author_reprocessed = params4.replace("-", " ").title()
                freq4=author_mean_pub_freq(results4,author_reprocessed)
                freq5=get_author_citation_frequency(results4,author_reprocessed)
                # fig6=get_collaboration_citation_frequency_stats_V2(results4,author_reprocessed)

            st.markdown('  ')
            st.markdown('  ')
            st.markdown(freq4)
            st.markdown(freq5)
            st.markdown(' --- ')
            st.markdown(f"<h6 style='text-align: center; color: #289c68'> All referenced papers by {author_reprocessed} :</h6>", unsafe_allow_html=True)
            df4=pd.DataFrame.from_dict(results4, orient='index', columns=['Title', 'Authors', 'Id', 'Year', 'Link', 'Category', 'Number_citations', 'Abstract'])[['Id','Category','Year','Title','Number_citations','Link']]
            df4['Year'] = df4['Year'].astype(int)
            df4.sort_values(by=['Year'], inplace=True,ascending=False)
            df4['Year'] = df4['Year'].astype(str)
            st.write(df4.set_index('Id'))

            # st.markdown(' --- ')
            # st.pyplot(fig6)

            #st.pyplot(chart6)

            # for key in results4:
            #     st.markdown('-- ' + str(results4[key]['Title']) + ', cited ' + str(results4[key]['Number_citations']) + ' times')
            #     st.markdown(str(results4[key]['Year'])+ ', ' + str(results4[key]['Authors']) + ', ' + str(results4[key]['Link']))
            #     st.markdown('Paper ID: ' + str(results4[key]['Id'])+ ' -- Category: ' + str(results4[key]['Category']))
            #     st.text('ABSTRACT -- ' + str(results4[key]['Abstract']))
            #     st.text(' ')
            #     st.text(' ')

with Tools:

    Translate,Summarize,Alert,Sensei = Tools.tabs(["Translator","Summarizer","New papers interestingness (soon)","AI/ML sensei (soon)"])

    with Translate:

        language_option = st.radio("Select a language : ",("Français", "Español", "Português"),)

        with st.form(key='params_for_api_tools_translate'):

            input5 = st.text_input('\> input exact paper ID to get its abstract translated (e.g. 1606-01781, 1706-03059, 1903-06236...)')

            if st.form_submit_button('Translate Abstract !'):

                params5 = input5.replace(' ','-').lower()

                if language_option == "Français":
                    #deepdipper_api_url5 = 'http://127.0.0.1:8000/translatefr?query='
                    deepdipper_api_url5 = 'https://deepdipper-rp6v7d7m4q-ew.a.run.app/translatefr'
                    st.markdown(f"<h6 style='text-align: center; color: #289c68'>Traduction en Français:</h6>", unsafe_allow_html=True)
                elif language_option == "Español":
                    #deepdipper_api_url5 = 'http://127.0.0.1:8000/translatees?query='
                    deepdipper_api_url5 = 'https://deepdipper-rp6v7d7m4q-ew.a.run.app/translatees'
                    st.markdown(f"<h6 style='text-align: center; color: #289c68'>Traducción en Español:</h6>", unsafe_allow_html=True)
                elif language_option == "Português":
                    #deepdipper_api_url5 = 'http://127.0.0.1:8000/translatepo?query='
                    deepdipper_api_url5 = 'https://deepdipper-rp6v7d7m4q-ew.a.run.app/translatepo'
                    st.markdown(f"<h6 style='text-align: center; color: #289c68'>Tradução em Português:</h6>", unsafe_allow_html=True)
                else:
                    st.markdown("Please select a language !")

                #response5 = requests.get(deepdipper_api_url5+params5)
                with st.spinner('Translating abstract...'):
                    #response5 = requests.get(deepdipper_api_url5+params5)
                    response5 = requests.get(deepdipper_api_url5, params=dict(query=params5))
                    results5 = response5.json()

                st.markdown(' ')
                st.markdown(results5['translated_text'])
                st.markdown(' ')
                st.markdown(' ')
                st.markdown(' --- ')
                st.markdown(' ')
                st.markdown('Original abstract :')
                st.markdown(' ')
                st.markdown(results5['original_text'])
                # for key in results5:
                #     value = results5[key]
                #     st.text(' ')
                #     st.markdown('  ')
                #     st.text(value['translated_text'])
                #     st.markdown('  ')
                #     st.text(' ')
                #     st.markdown('Original abstract :')
                #     st.text(value['original_text'])


    with Summarize:

        with st.form(key='params_for_api_tools_summarize'):

            input7 = st.text_input('\> input exact paper ID to get its abstract summarized into 2 to 4 sentences (e.g. 1606-01781, 1706-03059, 1903-06236...)')

            if st.form_submit_button('Summarize Abstract !'):
                params7 = input7.replace('.','-').lower()

                #deepdipper_api_url7 = 'http://127.0.0.1:8000/summarize?query='
                deepdipper_api_url7 = 'https://deepdipper-rp6v7d7m4q-ew.a.run.app/summarize'

                with st.spinner('Summarizing abstract...'):
                    #response7 = requests.get(deepdipper_api_url7+params7)
                    response7 = requests.get(deepdipper_api_url7, params=dict(query=params7))
                    results7 = response7.json()

                st.markdown(' ')
                st.markdown(results7['summary'])
                st.markdown(' ')
                st.markdown(' ')
                st.markdown(' --- ')
                st.markdown(' ')
                st.markdown('Original abstract :')
                st.markdown(' ')
                st.markdown(results7['original'])



    with Alert:

        st.markdown("coming soon, stay tuned !")

    with Sensei:

        st.markdown("coming soon, stay tuned !")

with About:
    st.markdown(' ')
    st.markdown("AI, ML and related fields related or fed by them are evolving at a rapid pace.", unsafe_allow_html=True)
    st.markdown("Research Pulse is a tool that helps in the exploration of research papers and their authors.", unsafe_allow_html=True)
    st.markdown("It is an all-in-one NLP toolkit that helps in finding most relevant content in a rapidly-evolving and abundant environment.", unsafe_allow_html=True)
    st.markdown('---')
    st.markdown('  ')
    col1, col2, col3, col4= st.columns(4)
    with col1:
        st.markdown("<h5 style='text-align: center; color: #289c68'>📊  Analytics dashboard  📈</h5>", unsafe_allow_html=True)
        st.markdown("Set of analytics views on the referenced database of papers.", unsafe_allow_html=True)
        st.markdown("Available aggregate and ranking views, with some key metrics dissected.", unsafe_allow_html=True)
        st.markdown("--tobedone: views by most recents, by categories, views of citations graph, pioneer papers identification, interactive queries...", unsafe_allow_html=True)
    with col2:
        st.markdown("<h5 style='text-align: center; color: #289c68'>🕵️  Search papers or authors  🗄️</h5>", unsafe_allow_html=True)
        st.markdown("Search for papers by keyword(s).", unsafe_allow_html=True)
        st.markdown("Search for authors by name(s).", unsafe_allow_html=True)
        st.markdown("Curated dataset of 774k research papers in areas related by close or by far to AI/ML.", unsafe_allow_html=True)
        st.markdown("Corpus of research papers published after 2000 and openly available on arXiv.org", unsafe_allow_html=True)

    with col3:
        st.markdown("<h5 style='text-align: center; color: #289c68'>🔎  Research a paper or an author  🧑🏽‍🔬</h5>", unsafe_allow_html=True)
        st.markdown("Look for paper details and pdf by inputting its ID (typically ctrl-c+v'ed from Search).", unsafe_allow_html=True)
        st.markdown("Look for specific author by inputting his/her full name (family-first name).", unsafe_allow_html=True)
        st.markdown("--tobedone: citation network graph parser, codes & algos repository per category...", unsafe_allow_html=True)
    with col4:
        st.markdown("<h5 style='text-align: center; color: #289c68'>🛠️  NLP-based toolbox  🤖</h5>", unsafe_allow_html=True)
        st.markdown("Set of tools to help in the exploration and accessibility of research areas.", unsafe_allow_html=True)
        st.markdown("Translater of abstracts (fr/es/pt), Summarizer of abstracts (2-3 sentences).", unsafe_allow_html=True)
        st.markdown("--tobedone: recent papers interestingness scorer, GPT AI/ML sensei...", unsafe_allow_html=True)
    st.markdown('---')
    st.markdown('  ')
    st.markdown("<h5 style='text-align: center; color: #289c68'>website developed by team DeepDipper</h5>", unsafe_allow_html=True)

st.markdown('---')
st.markdown("""
<p style='text-align: center; color: #289c68'>
    🤗 experiment with care | spread these tools 🙏
</p>
""", unsafe_allow_html=True)
st.markdown(f"""
<p style='text-align: center; color: #289c68'>
    page viewed {data['page_views']} times | built by team DeepDipper
</p>
""", unsafe_allow_html=True)
