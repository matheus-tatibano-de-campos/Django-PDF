import io
import os

from django.conf import settings
from django.http import FileResponse
from django.views.generic import View

from reportlab.pdfgen import canvas

# #####

from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from django.http import HttpResponse

from weasyprint import HTML


class IndexView(View):

    def get(self, request, *args, **kwargs):

        # Cria um arquivo para receber os dados e gerar o PDF
        buffer = io.BytesIO()

        # Criar o arquivo pdf
        pdf = canvas.Canvas(buffer)

        # Insere 'coisas' no PDF
        pdf.drawString(100, 100, "Geek University")

        # Quando acabamos de inserir coisas no PDF
        pdf.showPage()
        pdf.save()

        # Por fim, retornamos o buffer para o início do arquivo
        buffer.seek(0)

        # Faz o download do arquivo em PDF gerado
        # return FileResponse(buffer, as_attachment=True, filename='relatorio1.pdf')

        # Abre o PDF direto no navegador
        return FileResponse(buffer, filename='relatorio1.pdf')


class Index2View(View):
    def get(self, request, *args, **kwargs):
        texto = ['Geek University', 'Evolua seu lado geek', 'Programação Web com Python e Django']

        # Renderiza o template para uma string HTML
        html_string = render_to_string('relatorio.html', {'texto': texto})

        # Diretório para salvar o PDF
        output_dir = os.path.join(settings.BASE_DIR, 'media/tmp')
        os.makedirs(output_dir, exist_ok=True)

        pdf_path = os.path.join(output_dir, 'relatorio2.pdf')

        # Gera o PDF
        HTML(string=html_string).write_pdf(target=pdf_path)

        # Verifica se o PDF foi criado
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF não encontrado em {pdf_path}")

        # Retorna o PDF como resposta
        with open(pdf_path, 'rb') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="relatorio2.pdf"'
        return response