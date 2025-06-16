from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Lliga)
admin.site.register(Equip)
admin.site.register(Jugador)

#admin.site.register(Event)

class EventInline(admin.TabularInline):
    model = Event
    fields = ["temps","tipus","jugador","equip"]
    ordering = ("temps",)
    
class PartitAdmin(admin.ModelAdmin):
    # podem fer cerques en els models relacionats
    # (noms dels equips o títol de la lliga)
    search_fields = ["local__nom","visitant__nom","lliga__nom"]
    # el camp personalitzat ("resultats" o recompte de gols)
    # el mostrem com a "readonly_field"
    readonly_fields = ["resultat",]
    list_display = ["local","visitant","resultat","lliga","data"]
    ordering = ("-data",)
    inlines = [EventInline,]
    def resultat(self,obj):
        gols_local = obj.events.filter(
                        tipus="GOL",
                        equip=obj.local).count()
        gols_visit = obj.events.filter(
                        tipus="GOL",
                        equip=obj.visitant).count()
        return "{} - {}".format(gols_local,gols_visit)
 
admin.site.register(Partit,PartitAdmin)
