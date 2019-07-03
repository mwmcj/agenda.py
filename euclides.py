def euclides(n1,n2):
    quociente=[x for x in [n1,n2] if not [y for y in [n1,n2] if y>x]][0]//[x for x in [n1,n2] if not [y for y in [n1,n2] if y<x]][0]
    resto=[x for x in [n1,n2] if not [y for y in [n1,n2] if y>x]][0]%[x for x in [n1,n2] if not [y for y in [n1,n2] if y<x]][0]
    if not resto:
        return[x for x in [n1,n2] if not [y for y in [n1,n2] if y<x]][0]
    else:
        return euclides([x for x in [n1,n2] if not [y for y in [n1,n2] if y<x]][0],resto)
    
