def isAdmin(request):
    if request.user.role == 'DRH': return True
    else: return False