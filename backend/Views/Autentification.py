from django.contrib.auth import authenticate, logout, login
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated  # <-- Here
from backend.Formulaire import *
from backend.lector import *

class AuthView(APIView):
    errors = []
    
    def post(self, request):
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username = username, password = password)
            
            if user is not None:
                token = RefreshToken.for_user(user)
                return JsonResponse({'token': str(token.access_token)})
            else:
                return JsonResponse({"errors": 'Vos identidiants sont incorrectes'}, status = 401)

        else:
            return JsonResponse({"errors": "Les champs renseigner sont invalides !"})

    def delete(self, request):
        return JsonResponse()

# Inscrit le fichier dans le serveur 
def handle_uploaded_file(f):
    upload_dir = 'backend/questionnaires/'

    t = open( upload_dir + f.name, 'w')
    t.close()

    with open( upload_dir + f.name, 'wb+') as destination:
        print('ok 2')
        for chunk in f.chunks():
            destination.write(chunk)

    

class HelloView(APIView):
    # Permet de vérifier si le demandeur de la requête à bien fourni un token signé
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return JsonResponse(content)

    def post(self, request):
        if request.method == 'POST':
            print(request.POST.get('title'))
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                handle_uploaded_file(request.FILES['file'])
                return JsonResponse({'success': 'okay uploaded'})
        else:
            form = UploadFileForm()
        return JsonResponse({"ok": "ok"})