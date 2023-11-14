from django.shortcuts import render, get_object_or_404, redirect
from .forms import MoveForm
from .models import Equipement, Character

# Auxiliar function

def check_status(character, equipement):
    if character.etat == "affame" and equipement.id_equip == "mangeoire":
        return True
    elif character.etat == "fatigue" and equipement.id_equip == "nid":
        return True
    elif character.etat == "repus" and equipement.id_equip == "roue":
        return True
    elif character.etat == "endormi" and equipement.id_equip == "litiere":
        return True
    else:
        return False
    

def update_state(character, equipement):
    if equipement.id_equip == "mangeoire":
        character.etat = "repus"
    elif equipement.id_equip == "nid":
        character.etat = "endormi"
    elif equipement.id_equip == "roue":
        character.etat = "fatigue"
    elif equipement.id_equip == "litiere":
        character.etat = "affame"

# Create your views here.
def post_list(request):
    characters = Character.objects.all()
    equipements = Equipement.objects.all()
    return render(request, 'blog/post_list.html', {'characters': characters, 'equipements': equipements})

 
def character_detail(request, id_character):
    character = get_object_or_404(Character, id_character=id_character)
    ancien_lieu = get_object_or_404(Equipement, id_equip=character.lieu.id_equip)
    
    # form=MoveForm()
    form = MoveForm(request.POST, instance=character)

    error = None
    message = ""

    if request.method == "POST" and form.is_valid():
        form.save(commit=False)
        nouveau_lieu = get_object_or_404(Equipement, id_equip=character.lieu.id_equip)

        # Correct case
        if nouveau_lieu.disponibilite == "libre" and check_status(character, nouveau_lieu):
            error = False

            ancien_lieu.disponibilite = "libre"
            ancien_lieu.save()
            form.save()

            if nouveau_lieu.id_equip in ["roue", "mangeoire", "nid"]:
                nouveau_lieu.disponibilite = "occupe"             
            nouveau_lieu.save()  

            character.lieu = nouveau_lieu
            update_state(character, nouveau_lieu)
            character.save()

            message = character.id_character + " êtes maintenant à " + nouveau_lieu.id_equip

        # Error case
        else:
            error = True
            message = character.id_character + " ne pouvez pas aller à " + nouveau_lieu.id_equip

        # return redirect('character_detail', id_character=id_character)
        return render(request,
                  'playground/character_detail.html',
                  {'character': character, 'message': message, 'error': error, 'lieu': ancien_lieu, 'new_lieu': nouveau_lieu, 'form': form})
    
    else:
        form = MoveForm()
        return render(request,
                  'playground/character_detail.html',
                  {'character': character, 'lieu': ancien_lieu, 'form': form})

# def character_detail(request, pk):
#     character = get_object_or_404(Character, pk=pk)
#     return render(request, 'blog/character_detail.html', {'Character': character})

