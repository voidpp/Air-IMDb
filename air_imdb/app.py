from flask import Flask, request
from imdb import IMDb
from movie_data import MovieMap
from datetime import datetime
from dateutil import parser
import json
from voidpp_tools.json_config import JSONConfigLoader
import logging
import logging.config

config = JSONConfigLoader(__file__).load('air-imdb.config.json')

if config is None:
    print 'Config not found!!'

app = Flask('air_imdb')

logging.config.dictConfig(config['logger'])

logger = logging.getLogger('air_imdb')

@app.route('/')
def index():
    return 'zsomapelklod'

def get_movie_id(imdb, title, id):
    logger.info("Search for movie '%s', id = %s" % (title, title))
    movies = imdb.search_movie(title)
    for movie in movies:
        imdb_id = imdb.get_imdbMovieID(movie.movieID)
        logger.debug("Found movie %s (%s)" % ('', imdb_id))
        if imdb_id == id:
            return movie.movieID
    logger.info("Movie '%s' not found")
    return None

@app.route('/airdates', methods = ['POST'])
def airdates():
    if config is None:
        print 'Config not found!!'
        return '{}'

    mmap = MovieMap(config['cache_file'])
    imdb = IMDb('sql', uri = config['imdb_db_url'])
    show_list = json.loads(request.get_data())
    res = {}
    default = datetime(2016, 7, 15)
    try:
        for id in show_list:
            res[id] = None
            rdata = show_list[id]
            if rdata['imdb_id'] not in mmap.data:
                movie_id = get_movie_id(imdb, rdata['title'], rdata['imdb_id'])
                if movie_id:
                    mmap.data[rdata['imdb_id']] = movie_id

            if rdata['imdb_id'] not in mmap.data:
                print rdata
                continue

            movie = imdb.get_movie(mmap.data[rdata['imdb_id']])

            curr_season = rdata['after'][0]
            curr_episode = rdata['after'][1]
            next_start_season = curr_season
            next_start_episode = curr_episode

            if curr_episode+1 in movie['episodes'][curr_season]:
                next_start_episode = curr_episode + 1
            elif curr_season+1 in movie['episodes']:
                next_start_season = curr_season + 1
                next_start_episode = min(movie['episodes'][next_start_season].keys())
            else:
                continue

            try:
                next_episode = imdb.get_movie(movie['episodes'][next_start_season][next_start_episode].movieID)

                dates = []

                for release_date in next_episode['release dates']:
                    dates.append(parser.parse(release_date.split(':')[1], default = default))

                res[id] = dict(
                    air_en = min(dates).strftime('%Y-%m-%d'),
                    season = next_start_season,
                    episode = next_start_episode,
                )

            except KeyError as e:
                logger.exception("Error during movie info fetch")

    finally:
        mmap.save()

    return json.dumps(res) + '\n'
