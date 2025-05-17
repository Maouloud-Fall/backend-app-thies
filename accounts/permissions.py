from rest_framework import permissions


class IsEmployerOrReadOnly(permissions.BasePermission):
    """
    Permission personnalisée qui permet seulement aux employeurs de modifier une offre,
    mais autorise tout le monde à la voir.
    """

    def has_permission(self, request, view):
        # Autoriser les méthodes GET, HEAD ou OPTIONS (lecture seule)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Vérifier si l'utilisateur est authentifié et est un employeur
        return request.user.is_authenticated and request.user.is_employer

    def has_object_permission(self, request, view, obj):
        # Mêmes règles que has_permission
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated and request.user.is_employer