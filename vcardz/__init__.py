# Copyright 2015 Josh Watts
# Licensed under GPLv2, see LICENSE file for details
"""Python module for entity data (i.e. people, organizations) modeled
on `RFC 6350`_

.. _RFC 6350: https://tools.ietf.org/html/rfc6350
.. moduleauthor:: Josh Watts <josh.watts@gmail.com>
"""

from .parse import Parser  # noqa
from .builder import Builder  # noqa
from .vcard import *  # noqa
from .log import get_logger, set_logger # noqa


def scrub(stream, clean_results=True):
    # subway = nx.DiGraph()
    engine = Parser(stream)
    logger = get_logger()
    zombies = []
    people = []
    for card in engine:
        zombies.append(card)

    while 0 < len(zombies):
        logger.debug('zombies => %d', len(zombies))
        zombie = zombies.pop()
        buddy = None
        for ego in people:
            if zombie.match(ego):
                buddy = ego
                break

        if None == buddy:
            people.append(zombie)
            # subway.add_node(str(zombie.uid), zombie.compact())
        else:
            ego = zombie.merge(buddy)
            zombies.append(ego)
            try:
                people.remove(buddy)
            except:
                pass
            # people = people.difference([buddy])
            # subway.add_node(str(zombie.uid), zombie.compact())
            # subway.add_node(str(buddy.uid), buddy.compact())
            # subway.add_node(str(ego.uid), ego.compact())
            # subway.add_edge(str(zombie.uid), str(ego.uid))
            # subway.add_edge(str(buddy.uid), str(ego.uid))


    if True == clean_results:
        result = []
        for card in people:
            if card.clean():
                result.append(card)
    else:
        result = people

    # json_subway = json.dumps(nx.json_graph.node_link_data(subway))
    json_subway = ''

    return result, json_subway # map


def fscrub(stream, clean_results=True):
    # subway = nx.DiGraph()
    engine = Parser(stream)
    zombies = []
    people = []
    p_hash = {}
    n_hash = {}
    logger = get_logger()
    # subway = nx.DiGraph()

    # load input
    for card in engine:
        zombies.append(card)
        # card2 = card.clean()
        # if card2:
        #   zombies.append(card2)

    zombie = None
    while 0 < len(zombies) or zombie is not None:
        logger.debug('zombies => %d', len(zombies))
        if not zombie:
            zombie = zombies.pop()
        buddy = None

        zombie_features = zombie.features()
        for feat in zombie_features:
            key = feat[0] + ":" + feat[1]
            if key not in p_hash:
                p_hash[key] = zombie

        for feat in zombie_features:
            key = feat[0] + ":" + feat[1]
            creeper = p_hash[key]
            if creeper and creeper != zombie:
                buddy = creeper
                break

        if not buddy:
            for feat in zombie_features:
                feat_type = feat[0]
                feat_val = feat[1]
                key = feat[0] + ":" + feat[1]

                if key not in n_hash:
                    for ego in people:
                        ego_features = ego.features()
                        features_list = list(filter((lambda x: x if x[0] == feat_type\
                                                     else None),
                                                    ego_features))
                        for feat2 in features_list:
                            feat2_val = feat2[1]
                            if vCard.fmatch(feat_type, feat_val, feat2_val):
                                buddy = ego
                                break
                        if buddy:
                            break

                    if not buddy:
                        n_hash[key] = feat_val
                    else:
                        break
                if buddy:
                    break

        if not buddy:
            people.append(zombie)
            # subway.add_node(str(zombie.uid), zombie.compact())
            zombie = None
        else:
            ego = zombie.merge(buddy)
            logger.debug('buddy found')
            # subway.add_node(str(zombie.uid), zombie.compact())
            # subway.add_node(str(buddy.uid), buddy.compact())
            # subway.add_node(str(ego.uid), ego.compact())
            # subway.add_edge(str(zombie.uid), str(ego.uid))
            # subway.add_edge(str(buddy.uid), str(ego.uid))

            try:
                people.remove(buddy)
            except:
                pass
            ego_features = ego.features()
            for feat in ego_features:
                key = feat[0] + ":" + feat[1]
                p_hash[key] = ego
            zombie = ego

    result = []
    if True == clean_results:
        for doc in people:
            if doc.clean():
                result.append(doc)
    else:
        result = people

    # json_subway = json.dumps(json_graph.node_link_data(subway))
    json_subway = ''

    return result, json_subway
