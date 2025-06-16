from django.shortcuts import render, redirect

# Create your views here.


from django.http import HttpResponse
from django import forms
from django.views import generic

from .models import *

class MenuForm(forms.Form):
    lliga = forms.ModelChoiceField(queryset=Lliga.objects.all())
    #nom = forms.CharField()
    #cognoms = forms.CharField()
    #edat = forms.IntegerField()


def classificacio_menu(request):
    queryset = Lliga.objects.all()
    #form = MenuForm()
    #return render(request,"classificacio_menu.html",
    #		{"lligues":queryset,"form":form})

    # si hi ha dades, les processem
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            lliga = form.cleaned_data.get("lliga")
            # cridem a /classificacio/<lliga_id>
            return redirect('classificacio',lliga.id)

    # renderitzem formulari
    form = MenuForm()
    return render(request, "classificacio_menu.html",{
                    "lligues":queryset, # per renderitzar menú de links
                    "form":form,        # per renderitzar form desplegable
            })

def classificacio(request,lliga_id):
    lliga = Lliga.objects.get(pk=lliga_id)
    equips = lliga.equips.all()
    classi = []
 
    # calculem punts en llista de tuples (equip,punts)
    for equip in equips:
        punts = 0
        for partit in lliga.partits.filter(local=equip):
            if partit.gols_local() > partit.gols_visitant():
                punts += 3
            elif partit.gols_local() == partit.gols_visitant():
                punts += 1
        for partit in lliga.partits.filter(visitant=equip):
            if partit.gols_local() < partit.gols_visitant():
                punts += 3
            elif partit.gols_local() == partit.gols_visitant():
                punts += 1
        # si posem tupla, s'ordenarà pel primer dels criteris
        # en aquest cas, per punts (no per nom de l'equip)
        classi.append( (punts,equip.nom) )
    # ordenem llista
    classi.sort(reverse=True)
    return render(request,"classificacio.html",
                {
                    "classificacio":classi,
                    "lliga":lliga,
                })


class EquipForm(forms.ModelForm):
    class Meta:
        model = Equip
        exclude = ()

def crea_equip(request):
    form = EquipForm()

    # si hi ha dades, les processem
    if request.method == "POST":
        form = EquipForm(request.POST)
        if form.is_valid():
            equips = Equip.objects.filter(nom=form.cleaned_data.get("nom"))
            if equips.count()>0:
                return HttpResponse("ERROR: el nom de l'equip ja existeix.")
            form.save()
            return HttpResponse("L'equip s'ha creat correctament. <a href='/crea_equip'>Tornar al formulari</a>")

    # creem form si no hi ha dades
    return render(request,"crea_equip.html",{
        "form":form,
        })


class IndexView(generic.ListView):
    template_name = "lligafutbol/index.html"
    context_object_name = "latest_lliga_list"
    
    def get_queryset(self):
        """
        Return the last five published lligas.
        """
        return Lliga.objects.order_by("nom")[
            :5
        ]