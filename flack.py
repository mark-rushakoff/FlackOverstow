#!/usr/bin/env python

__author__ = "Mark Rushakoff"
__license__ = "MIT"

import sys
from optparse import OptionParser
from grabber import Grabber
from markov import markovchain

VERSION = "0.2"
VALID_TYPES = ('answers', 'questions', 'comments')

def die(msg):
    sys.stderr.write(sys.argv[0] + ": " + msg + "  Quitting.\n")
    sys.exit(1)

def main():
    parser = OptionParser(usage="%prog [opts] userid", version="%prog " + VERSION)
    parser.add_option("-u", "--user", action="store", type="int", dest="userid",
            help="Specify user ID whose posts to search (required or pass as unnamed argument)")
    parser.add_option("-s", "--site", action="store", type="string", 
            default='stackoverflow.com',  dest="site",
            help='Which site to query. (default: stackoverflow.com)')
    parser.add_option("-t", "--type", action="store", type="choice",
            default="answers", choices=VALID_TYPES, dest="query_type",
            help="What type of post to query. Options: " + ', '.join(VALID_TYPES) + " (default: answers)")
    parser.add_option("-c", "--chain-length", action="store", type="int", 
            dest="chain_length", default=6,
            help="Number of words to traverse in a single chain (default: 6)") 
    parser.add_option("-n", "--num-chains", action="store", type="int",
            dest="num_chains", default=25,
            help="Number of chains to traverse in output (default: 25)")
    parser.add_option("-k", "--api-key", action="store", type="string",
            dest="api_key", help="API key (default: none)")

    (options, args) = parser.parse_args()

    if len(args) == 1:
        try:
            options.userid = int(args[0])
        except ValueError:
            die("User ID must be an integer.")

    if options.userid is None or len(args) > 1:
        die("No user ID specified.")

    grabber = Grabber(options.site, options.userid)
    minimal_text = grabber.minimal_text(options.query_type)
    if not minimal_text:
        die("No posts found from that user.")
    spam = markovchain(' '.join(minimal_text), options.chain_length, options.num_chains)
    print spam

if __name__ == "__main__":
    main()
