from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Trabajo, Postulante

@receiver(post_save, sender=Trabajo)
def notificar_postulantes(sender, instance, created, **kwargs):
    if created:
        postulantes = Postulante.objects.filter(suscrito=True)
        destinatarios = [p.email for p in postulantes]

        if destinatarios:
            mensaje = f"""
            🌟 *Nueva Oportunidad Laboral Disponible* 🌟

            **{instance.titulo}** en *{instance.empresa}*
            
            📍 **Ubicación:** {instance.localidad}  
            🏢 **Categoría:** {instance.categoria}  
            ⏳ **Jornada:** {instance.tipo_jornada}  
            📌 **Modalidad:** {instance.modalidad}  
            👥 **Vacantes Disponibles:** {instance.cantidad}  

            🔎 *Descripción:*  
            {instance.descripcion if instance.descripcion else "No especificada"}

            📅 **Fecha de Publicación:** {instance.fecha.strftime('%d/%m/%Y')}

            👉 *Si estás interesado, revisa la plataforma para más detalles y postúlate cuanto antes!*

            ---
            *Este es un mensaje automático, por favor no respondas a este correo.*
            """

            send_mail(
                subject="📢 Nueva Oferta Laboral: " + instance.titulo,
                message=mensaje,
                from_email="lautarozarate826@gmail.com",
                recipient_list=destinatarios,
                fail_silently=False,
            )
