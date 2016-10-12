# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals, with_statement

import argparse

from neo4j.v1 import GraphDatabase, basic_auth
from literumi import spell

DRIVER = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "numbers"))

def create_links(lang, words=None, start=0, end=None):
    if not lang:
        raise ValueError('no language provided')

    session = DRIVER.session()

    if not words:
        if not end:
            raise ValueError('max number is required if no word list is given')

        words = (spell(n, lang=lang) for n in range(start, end + 1))

    for n1, word in enumerate(words, start=start):
        n2 = len(word.replace(' ', '').replace('-', '').replace(',', ''))
        cypher = '''
            MERGE (n1:Number {{value: {n1}}})
            MERGE (n2:Number {{value: {n2}}})
            CREATE UNIQUE (n1)-[e:LINK {{lang: '{lang}', word: '{word}'}}]->(n2)
            RETURN n1, e, n2;
        '''.format(
            n1=n1,
            n2=n2,
            lang=lang,
            word=word,
        )

        result = session.run(cypher)
        for record in result:
            print(record.values())

        if end and n1 >= end:
            break

    session.close()

def get_args():
    parser = argparse.ArgumentParser(description='load number word length graph data into Neo4j')
    parser.add_argument('-l', '--lang', required=True,
                        help='target language')
    parser.add_argument('-f', '--file',
                        help='file containing the words')
    parser.add_argument('-s', '--start', type=int, default=0,
                        help='first number to be processed')
    parser.add_argument('-e', '--end', type=int, default=1000,
                        help='last number to be processed')
    parser.add_argument('-v', '--verbose', action='count', default=0,
                        help='increase verbosity (specify multiple times for more)')

    return parser.parse_args()

def main():
    args = get_args()

    if args.file:
        with open(args.file, 'r') as f:
            words = filter(None, [word.strip() for word in f])
    else:
        words = None

    create_links(lang=args.lang, words=words, start=args.start, end=args.end)

if __name__ == '__main__':
    main()
