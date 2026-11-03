import secrets
import string
from math import log2

from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET


CHARACTER_GROUPS = {
    "lowercase": string.ascii_lowercase,
    "uppercase": string.ascii_uppercase,
    "numbers": string.digits,
    "symbols": "!@#$%^&*+-=_%?",
}
DEFAULT_LENGTH = 16


@require_GET
def home(request):
    return render(request, "home.html")


@never_cache
@require_GET
def password_generator(request):
    length = get_password_length(request.GET.get("length"))
    character_pool = get_character_pool(request.GET)
    groups = get_character_groups(request.GET)
    # Rejection sampling keeps every accepted password equally likely while
    # guaranteeing at least one character from each selected group.
    while True:
        password = "".join(secrets.choice(character_pool) for _ in range(length))
        if all(any(character in group for character in password) for group in groups):
            break
    strength = get_password_strength(length, request.GET)

    context = {
        "password": password,
        "length": length,
        "strength": strength,
    }
    response = render(request, "generated_password.html", context)
    response["Referrer-Policy"] = "no-referrer"
    return response


def get_password_length(length_value):
    try:
        length = int(length_value)
    except (TypeError, ValueError):
        return DEFAULT_LENGTH

    return min(max(length, 6), 32)


def get_character_groups(options):
    return [
        characters for name, characters in CHARACTER_GROUPS.items() if options.get(name)
    ] or [string.ascii_lowercase]


def get_character_pool(options):
    return "".join(get_character_groups(options))


def get_password_strength(length, options):
    groups = get_character_groups(options)
    pool_size = len(set(get_character_pool(options)))
    # Count strings containing every required group with inclusion-exclusion.
    # This accounts for the restrictions imposed by rejection sampling.
    possibilities = 0
    for mask in range(1 << len(groups)):
        omitted = [groups[index] for index in range(len(groups)) if mask & (1 << index)]
        remaining = pool_size - sum(len(set(group)) for group in omitted)
        possibilities += (-1) ** len(omitted) * remaining ** length
    entropy = log2(max(possibilities, 1))

    if entropy >= 80:
        return "Strong"

    if entropy >= 50:
        return "Medium"

    return "Weak"
