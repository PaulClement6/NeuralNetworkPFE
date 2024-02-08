import streamlit as st
import requests
#fichier contenant les fonction utiliser pour les boutons
###############Ouverture de camera#######################################


#fonction de changment de la variable d'etat pour activation de la caméra


###################################Activationb du filtre#######################################
#creation de variable de session pour activation du filtre
def active_cam():
    st.session_state.bouton_camera = not st.session_state.bouton_camera

#fonction permettant de changer la variable d'ouverture du filtre
def active_filre():
    st.session_state.mod = not st.session_state.mod
######################################activation  import postgre##################

def check_internet():
    try:
        requests.get('http://www.google.com', timeout=1)
        return True
    except requests.ConnectionError:
        return False
    
def active_affiche_data():
    st.session_state.bouton_postgre= not st.session_state.bouton_postgre 
