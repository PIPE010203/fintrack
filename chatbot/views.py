import logging
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Sum

logger = logging.getLogger(__name__)
from transacciones.models import Gasto, Ingreso
from openai import OpenAI
from datetime import date
import os, json

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@login_required
def chat_view(request):
    return render(request, 'chatbot/chat.html')

@login_required
@require_POST
def enviar_mensaje(request):
    data = json.loads(request.body)
    mensaje_usuario = data.get('mensaje', '')
    hoy = date.today()
    usuario = request.user

    total_gastos = Gasto.objects.filter(usuario=usuario, fecha__month=hoy.month).aggregate(t=Sum('monto'))['t'] or 0
    total_ingresos = Ingreso.objects.filter(usuario=usuario, fecha__month=hoy.month).aggregate(t=Sum('monto'))['t'] or 0
    balance = float(total_ingresos) - float(total_gastos)

    gastos_por_cat = {}
    for g in Gasto.objects.filter(usuario=usuario, fecha__month=hoy.month):
        gastos_por_cat[g.get_categoria_display()] = gastos_por_cat.get(g.get_categoria_display(), 0) + float(g.monto)

    contexto = f"""
Eres un asistente financiero personal para la app FinTrack.
El usuario se llama {usuario.username}.
Este mes ({hoy.strftime('%B %Y')}):
- Total ingresos: ${total_ingresos:,.0f} COP
- Total gastos: ${total_gastos:,.0f} COP
- Balance: ${balance:,.0f} COP
- Gastos por categoría: {gastos_por_cat}
Responde de forma concisa, amigable y en español. Da consejos útiles basados en los datos reales.
"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": contexto},
                {"role": "user", "content": mensaje_usuario}
            ],
            max_tokens=300
        )
        respuesta = response.choices[0].message.content
    except Exception as e:
        logger.error("Chatbot error for user %s: %s", request.user.username, str(e))
        respuesta = f"Error al conectar con IA: {str(e)}"

    return JsonResponse({'respuesta': respuesta})