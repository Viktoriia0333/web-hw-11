import os, sys, django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quotes_project.settings")
django.setup()

from quotes_project.mongo_models import Author as MongoAuthor, Quote as MongoQuote
from quotes_app.models import Author as PgAuthor, Quote as PgQuote

from mongoengine import connect
connect(db="quotes_db", host="mongodb+srv://v9bondarenko:password123@quotesproject.mcddql9.mongodb.net/?retryWrites=true&w=majority&appName=QuotesProject")

print("Міграція авторів…")
for m in MongoAuthor.objects:
    pg_author, created = PgAuthor.objects.get_or_create(
        fullname=m.fullname,
        defaults={
            "born_date": m.born_date,
            "born_location": m.born_location,
            "description": m.description
        }
    )
    action = "Додано" if created else "Оновлено"
    print(f"  {action} автора: {pg_author.fullname}")


print("Міграція цитат…")
for m in MongoQuote.objects:
    try:
        pg_author = PgAuthor.objects.get(fullname=m.author.fullname)
    except PgAuthor.DoesNotExist:
        print(f"  Пропущено цитату «{m.quote[:30]}…»: автор не знайдений")
        continue

    pg_quote, created = PgQuote.objects.get_or_create(
        quote=m.quote,
        author=pg_author,
        defaults={"tags": ",".join(m.tags)}
    )
    action = "Додано" if created else "Оновлено"
    print(f"  {action} цитату: «{m.quote[:30]}…»")

print("Міграція завершена.")
