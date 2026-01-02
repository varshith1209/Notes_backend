from celery import shared_task
from django.conf import settings
from openai import OpenAI
from .models import Note

client = OpenAI(api_key=settings.OPENAI_API_KEY)

@shared_task
def summarize_note_task(note_id):
    note = Note.objects.get(id=note_id)

    prompt = f"Summarize the following note in 3–5 sentences:\n\n{note.content}"

    response = client.chat.completions.create(
        model="gpt-4.1-mini",   # or "gpt-4o-mini", whichever you prefer
        messages=[
            {"role": "user", "content": prompt}
        ],
    )

    summary_text = response.choices[0].message.content   # <-- FIXED

    note.summary = summary_text
    note.save(update_fields=["summary"])

    return summary_text
