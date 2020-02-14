from django.shortcuts import render

from django.http import HttpResponse
from django.template.loader import render_to_string
#from weasyprint import HTML
import tempfile


def index(request):
    return render(request, 'index.html')
	

def doador_pdf(request):

    # queryset
    doador = Doador.objects.all()

    # context passed in the template
    context = {'doador': doador}

    # render
    html_string = render_to_string(
        'doador.html',context)
    html = HTML(string=html_string)
    result = html.write_pdf()

    # http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=doador_list.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())

    return response