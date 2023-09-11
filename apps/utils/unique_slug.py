from unidecode import unidecode


'''
random_string_generator is located here:
http://joincfe.com/blog/random-string-generator-in-python/
'''
def custom_slugify(title):
    symbol_mapping = (
        (' ', '-'),
        ('.', '-'),
        (',', '-'),
        ('!', '-'),
        ('?', '-'),
        ("'", '-'),
        ('"', '-'),
        ('ə', 'e'),
        ('ı', 'i'),
        ('İ', 'i'),
        ('i', 'i'),
        ('ö', 'o'),
        ('ğ', 'g'),
        ('ü', 'u'),
        ('ş', 's'),
        ('ç', 'c'),
    )
    title_url = title.strip().lower()

    for before, after in symbol_mapping:
        title_url = title_url.replace(before, after)

    return unidecode(title_url)

def unique_slug_generator(instance, new_slug=None, i=2):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = custom_slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=custom_slugify(instance.title),
                    randstr=i
                )
        a=i+1
        return unique_slug_generator(instance, new_slug=new_slug, i=a)
    return slug

def unique_slug_generator_with_name(instance, new_slug=None, i=2):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a name character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = custom_slugify(instance.name)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=custom_slugify(instance.name),
                    randstr=i
                )
        a=i+1
        return unique_slug_generator_with_name(instance, new_slug=new_slug, i=a)
    return slug
