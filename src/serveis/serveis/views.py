# -*- coding: utf-8 -*-
from pyramid.view import view_config
import json
import pymongo

STORAGE_FILENAME = "/var/wwwdata/xat.txt"

@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'Serveis/JsonXat'}

@view_config(route_name='jsontest', renderer='jsonp')
def jsontest(request):
    dades = {"project":"Serveis/JsonXat", "author":"enricus" }
    return dades

"""
    JSONXAT
"""
@view_config(route_name='xat_get_canals_ws', renderer='jsonp')
def xat_get_canals_ws(request):
    dades = [ "principal", "test" ]
    return dades

@view_config(route_name='xat_get_canal_ws', renderer='jsonp')
def xat_get_canal_ws(request):
    #canal = request.matchdict['canal_id']
    # TODO: recuperar info d'un canal concret
    try:
        canal = request.GET.get("canal")
        if not canal:
            canal = request.json_body["canal"]
        if canal != "principal":
            return {"status":False, "missatge":"canal inexistent" }
    except Exception as e:
        print type(e).__name__
        print e.args
        return {"status":False, "missatge":"error intern"}
    missatges = []
    file = open(STORAGE_FILENAME)
    for linia in file:
        l = linia.split("\t")
        if len(l)>1:
            remitent = l[0]
            msg = l[1].strip()
            reg = { "remitent":remitent, "missatge":msg }
            missatges.append( reg )

    return {"status":True, "missatges":missatges}



@view_config(route_name='xat_set_missatge_ws', renderer='jsonp')
def xat_set_missatge_ws(request):
    try:
        #print request.GET
        # ho intentem per GET (JSONP)
        remitent = request.GET.get("remitent")
        missatge = request.GET.get("missatge")
        if remitent and missatge:
            if remitent.strip() and missatge.strip():
                linia = remitent + "\t" + missatge 
        else:
            # ho intentm per POST (JSON)
            dades = request.json_body
            linia = dades["remitent"] + "\t" + dades["missatge"] 
            # TODO: retornar amb POST-JSON (no JSONP)
        if "<" in linia or "\n" in linia:
            return {
                "servei":"xat",
                "canal":"principal",
                "status":False,
                "missatge":"ERROR: caracters ilegals"
            }
        file = open(STORAGE_FILENAME,"a+")
        file.write(linia+"\n");
        file.close()
            
    except ValueError:
        return {"servei":"xat",
		"canal":"principal",
		"status":False,
		"missatge":"ERROR: JSON incorrecte"
        }
    except Exception as e:
        print type(e).__name__
        print e.args
        return {"servei":"xat",
		"canal":"principal",
		"status":False,
		"missatge":"ERROR desonegut: " + type(e).__name__
        }
    
    return {	"servei":"xat",
		"canal":"principal",
		"status":True,
		"missatge":"missatge enregistrat correctament"
    }
    
"""
    FEEDBACK APP
"""
# https://pythonhosted.org/pyramid_simpleform/
from formencode import Schema, validators
from pyramid_simpleform import Form
from pyramid_simpleform.renderers import FormRenderer

class FeedbackSchema(Schema):
    #http://www.formencode.org/en/latest/modules/validators.html
    allow_extra_fields = True
    filter_extra_fields = True
    name = validators.UnicodeString(max=5, min=1)
    value = validators.Int(min=1, max=1000)
    # TODO: textarea?
    type = validators.OneOf(["bug/error","improvement/millora"])

class Feedback(object):
    pass

@view_config(route_name='feedback', renderer='feedback.mako')
def feedback(request):
    #form = Form( request, defaults={"name":"..."}, schema=FeedbackSchema() )
    form = Form( request, schema=FeedbackSchema() )
    #print dir(MyRenderer(form))
    if form.validate():
        obj = form.bind( Feedback() )
        #...
        print obj.__dict__
        return {"message":"Feedback recorded successfuly"}
    return {"message":"Please fill the form","renderer":FormRenderer(form) }

@view_config(route_name='set_report_ws', renderer='json')
def set_report_ws(request):
    try:
        client = pymongo.MongoClient()
        db = client.vm_feedback
        cols = db.collection_names()
        
        idata = request.json_body
        return { "status":False, "message":"Service not implemented yet" }
        
    except Exception as e:
        print type(e).__name__
        print e.args
        return {"service":"vm_feedback",
		"status":False,
		"message":"ERROR: " + type(e).__name__ + " args=" + str(e.args)
        }
    
    return {"status":True,"collections":cols}

