import streamlit as st
#fichier contenant les fonction utiliser pour les boutons
###############Ouverture de camera#######################################
# Ajout de variable session permmettant d'ouvrir la camera
if "bouton" not in st.session_state:
    st.session_state.bouton = False


#fonction de changment de la variable d'etat pour activation de la caméra
def active_cam():
    st.session_state.bouton = not st.session_state.bouton

###################################Activationb du filtre#######################################
#creation de variable de session pour activation du filtre
if "mod" not in st.session_state:
    st.session_state.mod = False

#fonction permettant de changer la variable d'ouverture du filtre
def active_filre():
    st.session_state.mod = not st.session_state.mod
######################################activation  import postgre##################
if "bouton_postgre" not in st.session_state:
    st.session_state.bouton_postgre = False
def active_affiche_data():
    st.session_state.bouton_postgre= not st.session_state.bouton_postgre 