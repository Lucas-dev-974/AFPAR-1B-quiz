// Création d'une fonction stocké dans une variable qui vas permettre de gérer les données dans le localStorage
const storage ={
    // Retourne un objet JSON des données essentiels à l'app tel que le token, les informations utilisateurs (email, nom, prénom..), la liste des sessions récuperer....
    state: function(){
        let state = {}
        if(localStorage.getItem('quizz-app-storage')) state = JSON.parse(localStorage.getItem('quizz-app-storage'))
        return state
    },

    // Définie une valeur 
    setState: function(name, value) {
        let state = storage.state()
        state[name] = value
        storage.registerState(state)
    },

    registerState: function(state) {
        const jsonstrstate = JSON.stringify(state)
        localStorage.setItem('quizz-app-storage', jsonstrstate)
    },

}

const request = async (uri, params, method = 'POST') => {
    let token = storage.state().token ?? ''

    if (params instanceof FormData) {
        params = {
            body: params
        }
    }
    else{
        params = {
            data: params
        }
    }

    let options = {
        method: method,
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=UTF-8',
            'Authorization': `Bearer ${token}`,
        },
        ...params,
    }

    return await fetch(uri, options)
}   

const jsonToFormData = (json) => {
    // Créer un formulaire 
    const data = new FormData()
    
    if(json != null){
        try{
            // Pour chaque entrer du json on la récupère dans params qui lui est array qui contien en 0 le nom donner et en 1 la valeur  
            Object.entries(json).forEach(param => {
                data.append(param[0], param[1])
            });
            
        }catch(error){
            console.log(error);
            alert('Désoler une erreur est survenue veuillez recharger la page !')
        }
    }

    return data
}

// Permet de montrer qu'1 seul et unique élément HTML fesant parti d'une liste d'éléments 
const paging = (pages_elements, show_page_id) => {
    // afficher pages_elements pour voir ce que c'est -> (HTMLelement)
    // On parcour la listes des pages 
    pages_elements.forEach(page => {
        // Si l'id de l'élément n'est pas = à l'idée renseigner alors on cache l'élément
        if(page.id != show_page_id) page.style.display = 'none'
        // Sinon on affiche l'élément si les ID sont égaux
        else page.style.display = 'block'
    })
}

const listPage = [
    document.getElementById('page-1'),

]