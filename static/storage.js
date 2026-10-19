const KEYS = {
    favorites: 'cinescope.favorites',
    watched: 'cinescope.watched'
};

function getList(key) {
    const data = localStorage.getItem(key);
    return data ? JSON.parse(data) : [];
}

function toggleMovieInList(key, movieId, movieData = null) {
    let list = getList(key);
    const index = list.findIndex(item => item.id === movieId);

    if (index > -1) {
        list.splice(index, 1);
        localStorage.setItem(key, JSON.stringify(list));
        return false; 
    } else {
        const itemToSave = movieData ? { id: movieId, ...movieData } : { id: movieId };
        list.push(itemToSave);
        localStorage.setItem(key, JSON.stringify(list));
        return true; 
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const favorites = getList(KEYS.favorites);
    const watched = getList(KEYS.watched);

    document.querySelectorAll('.btn-favorite').forEach(btn => {
        const id = parseInt(btn.dataset.id);
        if (favorites.some(item => item.id === id)) {
            btn.classList.add('bg-red-600', 'text-white');
            btn.innerText = '❤️ Favorito';
        }
    });

    document.querySelectorAll('.btn-watched').forEach(btn => {
        const id = parseInt(btn.dataset.id);
        if (watched.some(item => item.id === id)) {
            btn.classList.add('bg-green-600', 'text-white');
            btn.innerText = '✅ Assistido';
        }
    });
});

function favoriteMovie(movieId, title, posterPath) {
    const movieData = { title, poster_path: posterPath };
    const isAdded = toggleMovieInList(KEYS.favorites, movieId, movieData);
    const btn = document.querySelector(`.btn-favorite[data-id="${movieId}"]`);
    
    if (isAdded) {
        btn.classList.add('bg-red-600', 'text-white');
        btn.innerText = '❤️ Favorito';
    } else {
        btn.classList.remove('bg-red-600', 'text-white');
        btn.innerText = '🤍 Favoritar';
    }
}

function watchMovie(movieId, title, posterPath) {
    const movieData = { title, poster_path: posterPath };
    const isAdded = toggleMovieInList(KEYS.watched, movieId, movieData);
    const btn = document.querySelector(`.btn-watched[data-id="${movieId}"]`);
    
    if (isAdded) {
        btn.classList.add('bg-green-600', 'text-white');
        btn.innerText = '✅ Assistido';
    } else {
        btn.classList.remove('bg-green-600', 'text-white');
        btn.innerText = '👁️ Assistido';
    }
}
