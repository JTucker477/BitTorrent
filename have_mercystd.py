#!/usr/bin/python

# This is a dummy peer that just illustrates the available information your peers 
# have available.

# You'll want to copy this file to AgentNameXXX.py for various versions of XXX,
# probably get rid of the silly logging messages, and then add more logic.

import random
import logging

from messages import Upload, Request
from util import even_split
from peer import Peer

class have_mercystd(Peer):
    def post_init(self):
        print(("post_init(): %s here!" % self.id))
        self.dummy_state = dict()
        self.dummy_state["cake"] = "lie"

        self.optimistic = [0, None]    

    def requests(self, peers, history):
        """
        peers: available info about the peers (who has what pieces)
        history: what's happened so far as far as this peer can see

        returns: a list of Request() objects

        This will be called after update_pieces() with the most recent state.
        """

        # self.from_id = from_id  # who did the agent download from?
        # self.to_id = to_id      # Who downloaded?
        # self.piece = piece      # Which piece?
        # self.blocks = blocks    # How much did the agent download?

        # Loop through the history and find who has downloaded to who

        # Downloads is who we've gotten it from. From some other peer, to us! 

        
        # A list of lists. Each list represents a round (round 0 is history.downloads[0]). Then, the different downloads in the round are in the list 
        # history.downloads = [[[Download(from_id=Seed0, to_id=have_mercystd0, piece=0, blocks=1)], [], [], [Download(from_id=Seed0, to_id=have_mercystd0, piece=1, blocks=1), Download(from_id=have_mercystd3, to_id=have_mercystd0, piece=0, blocks=1)], [Download(from_id=Seed0, to_id=have_mercystd0, piece=1, blocks=1)]]

        
  

     
        # if len(history.downloads) != 0:
        #     logging.debug('cool')
        #     logging.debug(history.downloads[0])

            # for i in range(3):
            #     if i < len()


            # for i in range(len(history.downloads)):
            #     if len(history.downloads[0]) != 0:

            #         logging.debug('start1')
            #         temp = history.downloads[0]

            #         logging.debug(type(temp[0]))
            #         # have_mercystd3
            #         logging.debug(temp[0].to_id)

            #         # Focus on This! We are interested in this! 
            #         # Seed0
            #         # # logging.debug(temp[i].from_id)
            #         # dlhist[temp[i].from_id] += 
            #         # 1
            #         logging.debug(temp[0].blocks)
            #         logging.debug('stop1')
                

        needed = lambda i: self.pieces[i] < self.conf.blocks_per_piece
        needed_pieces = list(filter(needed, list(range(len(self.pieces)))))
        np_set = set(needed_pieces)  # sets support fast intersection ops.


        logging.debug("%s here: still need pieces %s" % (
            self.id, needed_pieces))

        logging.debug("%s still here. Here are some peers:" % self.id)
        for p in peers:
            logging.debug("id: %s, available pieces: %s" % (p.id, p.available_pieces))

        logging.debug("And look, I have my entire history available too:")
        logging.debug("look at the AgentHistory class in history.py for details")
        logging.debug(str(history))

        requests = []   # We'll put all the things we want here
        # Symmetry breaking is good...
        random.shuffle(needed_pieces)
       
        # Sort peers by id.  This is probably not a useful sort, but other 
        # sorts might be useful
        peers.sort(key=lambda p: p.id)
        # request all available pieces from all peers!
        # (up to self.max_requests from each)

   
        for peer in peers:
            av_set = set(peer.available_pieces)
            isect = av_set.intersection(np_set)
            n = min(self.max_requests, len(isect))
            # More symmetry breaking -- ask for random pieces.
            # This would be the place to try fancier piece-requesting strategies
            # to avoid getting the same thing from multiple peers at a time.
            for piece_id in random.sample(isect, n):
                # aha! The peer has this piece! Request it.
                # which part of the piece do we need next?
                # (must get the next-needed blocks in order)
                start_block = self.pieces[piece_id]
                r = Request(self.id, peer.id, piece_id, start_block)
                requests.append(r)
        

        return requests

    def uploads(self, requests, peers, history):
        """
        requests -- a list of the requests for this peer for this round
        peers -- available info about all the peers
        history -- history for all previous rounds

        returns: list of Upload objects.

        In each round, this will be called after requests().
        """

        round = history.current_round()

    #    requests = {A , B , E , G , Z}
    #    download1 = {A, E, F}
    #    download2 = {G, H, T , I }
        req_dict = {}
        # Creating a dictionary with all of the requests
        for request in requests:
            if request.requester_id not in req_dict:
                req_dict[request.requester_id] = 0 
        # For the last two rounds
        # round 0: []
        # round 1: [[] ]
        # downloads = [[] , [] ]
        # At most back 2 rounds 
        for i in range(min(2, len(history.downloads))):
                # For each download in each round
                for download in history.downloads[history.current_round() - (i +1)]:
                    # if the download is in the requests, increase the amount of blocks in req_dict
                    if download.from_id in req_dict:
                        req_dict[download.from_id] += download.blocks
        req_helped = []
        for i in req_dict.items():
            req_helped.append(i)
        req_helped.sort(reverse=True, key=lambda p: p[1])
        logging.debug("here")
        logging.debug(req_helped)
        top_three = req_helped[:min(3, len(req_helped))]
        
        # Go through the top three, and get rid of any that is 0. Then, just create a list of names
        i = 0
        while(True):
            if i >= len(top_three):
                break
            if top_three[i][1] == 0:
                top_three.remove(top_three[i])
            else:
                top_three[i] = top_three[i][0]
            i+=1


        # logging.debug(f"Available: {available}")
        logging.debug("%s again.  It's round %d." % (
            self.id, round))
        # One could look at other stuff in the history too here.
        # For example, history.downloads[round-1] (if round != 0, of course)
        # has a list of Download objects for each Download to this peer in
        # the previous round.

        if len(requests) == 0:
            logging.debug("No one wants my pieces!")
            chosen = []
            bws = []
        else:

            logging.debug("Still here: uploading to a random peer")
            # change my internal state for no reason
            self.dummy_state["cake"] = "pie"

            # request = random.choice(requests)
            # chosen = [request.requester_id]
            chosen = []
            # Evenly "split" my upload bandwidth among the one chosen requester
    
            # For each request, see which is in the top 3. and they are not equal to 0
            for request in requests:
                if request.requester_id in top_three:
                    chosen.append(request)

            
            # Randomly chose 1 person to keep for 3 rounds
            if self.optimistic[0] == 0:
                # If it's long enough, we don't want to pick a neighbor that was in our top three
                logging.debug("heller 3")

                # the requester ids in the list of request objects
                requester_ids= set([request.requester_id for request in requests])
                # The people who are not in the top three are eligible for optimistic unchoking
                opt_avail = list(requester_ids.symmetric_difference(set(top_three)))
                # If there are people left
                if len(opt_avail) != 0:
                    random_request = random.choice(opt_avail)
                    logging.debug("yuh")
                    # Find the original request object to put in
                    for request in requests:
                        if request.requester_id == random_request:
                            chosen.append(request)
                            self.optimistic[1] = request
                
            self.optimistic[0] = (self.optimistic[0] + 1) % 3
            chosen = chosen + [self.optimistic[1]]
            bws = even_split(self.up_bw, len(chosen))

        # create actual uploads out of the list of peer ids and bandwidths
        uploads = [Upload(self.id, peer_id, bw)
                   for (peer_id, bw) in zip(chosen, bws)]
            
        return uploads


# [Request(requester_id=have_mercystd0, peer_id=have_mercystd4, piece_id=1, start=1), Request(requester_id=have_mercystd1, peer_id=have_mercystd4, piece_id=1, start=1), Request(requester_id=have_mercystd2, peer_id=have_mercystd4, piece_id=1, start=1), Request(requester_id=have_mercystd3, peer_id=have_mercystd4, piece_id=1, start=1)]



        # for peer in peers:
        #     for piece in peer.available_pieces:
        #         if piece not in dictionary.keys():
        #             dictionary[piece] = 1
        #         else:
        #             dictionary[piece] += 1

        # available = []
        # for i in dictionary.items():
        #     available.append(i)

        # #logging.debug(f"Available: {available}")

        # available.sort(key=lambda p: p[1])
#  dlhist = {} 
#         if len(history.downloads) != 0:
#             for i in range(min(3, len(history.downloads))):
#                 for j in range(len(history.downloads[i])):
#                     if history.downloads[i][j].from_id in dlhist:
#                         dlhist[history.downloads[i][j].from_id] += history.downloads[i][j].blocks
#                     else: 
#                         dlhist[history.downloads[i][j].from_id] = history.downloads[i][j].blocks
#         helped = []
#         for i in dlhist.items():
#             helped.append(i)
#         helped.sort(reverse=True, key=lambda p: p[1])



            # # For each of the top three helpers
            # for i in range(len(top_three)):
            #     # For all of the requests, check if any are from the top three
            #     logging.debug("heller 1")

            #     for request in requests:
            #         logging.debug(top_three[i][0])
            #         logging.debug(request.requester_id)
            #         if top_three[i][0] == request.requester_id:
            #             logging.debug("heller 2")
            #             chosen.append(request.requester_id)
            #             break