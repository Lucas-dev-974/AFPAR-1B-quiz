const storage ={
    state: function(){
        let state = {}
        if(localStorage.getItem('quizz-app')) state = JSON.parse(localStorage.getItem('quizz-app'))
        return state
    },

    setState: function(name, value) {
        let state = storage.state()
        state[name] = value
        storage.registerState(state)
    },

    registerState: function(state) {
        const jsonstrstate = JSON.stringify(state)
        localStorage.setItem('quizz-app', jsonstrstate)
    },

    strState: function(){
        return JSON.stringify(storage.state())
    }
}

const request = async (uri, params, method = 'POST') => {
    let token = null

    params.append('csrfmiddlewaretoken', '{{csrf_token}}')
    
    let options = {
        method: method,
        header: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Origin': '',
            'Host': window.location.host,
            'Authorization': `Token ${token}`,
        },
        body: params,

    }

    if(storage.state().token){
        token = storage.state().token
        options.header.Authorization = 'Token ' + token
    }else console.log('aucun token renseigner');

    

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