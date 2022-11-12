// Création d'une fonction storage (stockage) dans une variable qui vas permettre de gérer les données dans le localStorage
const storage ={
    // Retourne un objet JSON des données essentiels à l'app tel que le token, les informations utilisateurs (email, nom, prénom..), la liste des sessions récuperer....
    state: function(){
        // Instanciation d'un objet
        let state = {}

        // Si dans le localStorage on à un item quizz-app-storage 
        // Alors on récupère le stockage dans notre variable state
        if(localStorage.getItem('quizz-app-storage')) state = JSON.parse(localStorage.getItem('quizz-app-storage'))

        // Et enfin on retourne notre object
        return state
    },

    // Définie une valeur 
    setState: function(name, value) {

        // Récupère le stoackage
        let state = storage.state()

        // Attribut la key:value donner en paramètres au stockage
        state[name] = value

        // Réenregistre les stockage dans le localstorage
        storage.registerState(state)
    },

    // Permet d'enregistrer un json dans le localStorage
    registerState: function(state) {
        const jsonstrstate = JSON.stringify(state)
        localStorage.setItem('quizz-app-storage', jsonstrstate)
    },

}

//  Nous permet de faire des requêtes sans ce soucier d'incerer le token qui se trouve dans le stockage
const request = async (uri, params, method = 'POST') => {

    // Il eciste des condition courte qui peuvent se itervenir lors d'une déclaration de variable,
    // comme si dessous, syntaxe condition courte : let variable = condition ? si oui : si non 
    const token = storage.state().token ?? ''
    const tokenAuthorization = token != '' ? {'Authorization':  ` Token  ${token} `} : ''
        
    if(method != 'GET')
        params = (params instanceof FormData) == true ? { body: params } : { body: JSON.stringify(params) }
    else
        params = { params: params }


    let options = {
        method: method,
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            ...tokenAuthorization
        },
        ...params
    }

    console.log('options de la requêtes:', options)
    
    return await fetch(uri, options)
}   

const jsonToFormData = (json) => {
    // Créer un formulaire 
    const data = new FormData()
    
    try{
        // Pour chaque entrer du json on la récupère dans params qui lui est array qui contien en 0 le nom donner et en 1 la valeur  
        Object.entries(json).forEach(param => {
            data.append(param[0], param[1])
        });
        
    }catch(error){
        console.log(error);
        alert('Désoler une erreur est survenue veuillez recharger la page !')
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