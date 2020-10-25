from django.utils.safestring import mark_safe

def initWithData(DATA, prefix):#this is for initing(and needed in a list of formsets) a formset with a DATA dict, appending the formset prefix,
    initializedDATA = {}

    for key in DATA.keys():
        initializedDATA[prefix +"-"+ key] = DATA[key]
    
    return initializedDATA

def formsets_factory(formset, DEFAULT_DATA = None):
    formsets = Formsets
    formsets.formset = formset
    if DEFAULT_DATA:
        formsets.DEFAULT_DATA = DEFAULT_DATA
    return formsets

def to_html_input_tag(id,type,name,value):#think a better name, or use built_in function of django no recuerdo el name
    #return '<input type="' + type + '" name="' + name + '" value="' + value + '" id="' + id + '">'
    return '<input id="' + id + '" type="' + type + '" name="' + name + '" value="' + value + '">'#cambiar esto por un string.format(variables)


class Formsets():
    formsetsDict = {}
    formset = None#cambiar esto por algo q sea razonable
    prefix = "formsets"
    
    TOTAL_FORMSETS = 2
    DEFAULT_DATA = {#defaul data para inicializar todos los formsets, puede incluir TOTAL_FORMSETS o no
        'TOTAL_FORMS': '2',
        'INITIAL_FORMS': '0',
        }

    def __init__(self, DATA , prefix = None):
        TOTAL_FORMSETS = DATA.get(self.prefix+"-TOTAL_FORMSETS")#poner esto y su asignacion condicional pa otra funcion q pueda ser usada con cualquier parametro
        if TOTAL_FORMSETS:
            self.TOTAL_FORMSETS = int(TOTAL_FORMSETS)

        if prefix:#revisar si se puede hacer algo como esto #self.label_suffix = label_suffix if label_suffix is not None else _(':')
            self.prefix = prefix
        
        for index in range(self.TOTAL_FORMSETS):
            #self.formsetsDict[prefix+str(index)] = formset(initWithData(DATA, prefix+str(index)), prefix = prefix+str(index))            
            self.formsetsDict[self.prefix+'-'+str(index)] = self.formset(DATA or initWithData(self.DEFAULT_DATA, self.prefix+'-'+str(index)), prefix = self.prefix+'-'+str(index))#TODO:take this out, to where is instantiated the class, that way isnt needed too many args
    
    def __iter__(self):
        return self.formsets_iterator(self)
    
    #def __iter__(self):        #si el iter pudiera ser asi estaria mucho mejor, pero creo q necesita la funcion getitem para funcionar
    #    for name in self.fields:#la idea es usar yield en vez de return
    #        yield self[name]
    
    def is_valid(self):
        result = True
        for formset in self.formsetsDict.values():
            if (formset.is_valid() == False):
                return False
            else:
                return result

    def management_form(self):#cambiar esto y ponerlo en una funcion aparte y retornarla en __str__, y encapsular management_form o algo asi
        management_form = ''
        management_form +=  to_html_input_tag(id = "id_"+self.prefix+"-TOTAL_FORMSETS" ,type = "hidden",name = self.prefix+"-TOTAL_FORMSETS",value = str(self.TOTAL_FORMSETS))
        return mark_safe(management_form) 

    def save(self):#not tested, and need to throw errors if formset is invalid too
        for formset in self.formsetsDict.values():
            if formset.is_valid():
                formset.save()
        return False
    
    def size(self):
        return len(self.formsetsDict)
 
    class formsets_iterator():
        ''' Iterator class '''
        def __init__(self, formset):
            # Team object reference
            self._formset = formset
            # member variable to keep track of current index
            self._index = 0
        
        def __next__(self):
            ''''Returns the next value from team object's lists '''
            if self._index < (len(self._formset.formsetsDict)) :
                result = next( v for i, v in enumerate(self._formset.formsetsDict.values()) if i == self._index )#revisar q hace esto exactamente, UPDT ya se lo q hace y parece funcionar cool
                self._index +=1
                return result
            # End of Iteration
            raise StopIteration
