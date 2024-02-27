# guest_management/context_processors.py

def recepcionista_context(request):
    is_recepcionista = request.user.is_authenticated and request.user.groups.filter(name='Recepcionistas').exists()
    return {'is_recepcionista': is_recepcionista}