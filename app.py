from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from flask import Flask, render_template, request

app = Flask(__name__)


@dataclass(frozen=True)
class Movie:
    title: str
    genre: str
    mood: str
    year: int
    description: str


MOVIES: tuple[Movie, ...] = (
    Movie("Интерстеллар", "sci-fi", "thoughtful", 2014, "Эпичное космическое путешествие о времени и семье."),
    Movie("Достать ножи", "detective", "light", 2019, "Ироничный детектив с неожиданными поворотами."),
    Movie("1+1", "comedy", "feel-good", 2011, "Тёплая история дружбы, которая поднимает настроение."),
    Movie("Одержимость", "drama", "intense", 2014, "Жёсткая драма о цене совершенства в музыке."),
    Movie("Человек-паук: Через вселенные", "animation", "energetic", 2018, "Стильная анимация с динамичным сюжетом."),
    Movie("Остров проклятых", "thriller", "dark", 2010, "Психологический триллер с мрачной атмосферой."),
    Movie("Зелёная книга", "drama", "feel-good", 2018, "Дорожная история о дружбе и принятии."),
    Movie("Паразиты", "thriller", "thoughtful", 2019, "Остроумная социальная сатира с напряжением."),
)

GENRES = {
    "": "Любой жанр",
    "sci-fi": "Фантастика",
    "detective": "Детектив",
    "comedy": "Комедия",
    "drama": "Драма",
    "animation": "Анимация",
    "thriller": "Триллер",
}

MOODS = {
    "": "Любое настроение",
    "feel-good": "Хочу что-то доброе",
    "light": "Хочу что-то лёгкое",
    "thoughtful": "Хочу подумать",
    "energetic": "Хочу драйв",
    "intense": "Хочу напряжение",
    "dark": "Хочу что-то мрачное",
}


def recommend(genre: str, mood: str) -> list[Movie]:
    filtered: Iterable[Movie] = MOVIES
    if genre:
        filtered = (movie for movie in filtered if movie.genre == genre)
    if mood:
        filtered = (movie for movie in filtered if movie.mood == mood)
    recommendations = list(filtered)

    if recommendations:
        return recommendations

    # fallback: if strict filters return nothing, relax one filter step-by-step
    if genre:
        by_genre = [movie for movie in MOVIES if movie.genre == genre]
        if by_genre:
            return by_genre
    if mood:
        by_mood = [movie for movie in MOVIES if movie.mood == mood]
        if by_mood:
            return by_mood

    return list(MOVIES[:4])


@app.route("/", methods=["GET", "POST"])
def index() -> str:
    selected_genre = ""
    selected_mood = ""
    movies: list[Movie] = []

    if request.method == "POST":
        selected_genre = request.form.get("genre", "")
        selected_mood = request.form.get("mood", "")
        movies = recommend(selected_genre, selected_mood)

    return render_template(
        "index.html",
        genres=GENRES,
        moods=MOODS,
        movies=movies,
        selected_genre=selected_genre,
        selected_mood=selected_mood,
    )


if __name__ == "__main__":
    app.run(debug=True)
