
from sample_players import DataPlayer


class CustomPlayer(DataPlayer):
    """ Implement your own agent to play knight's Isolation

    The get_action() method is the only required method for this project.
    You can modify the interface for get_action by adding named parameters
    with default values, but the function MUST remain compatible with the
    default interface.

    **********************************************************************
    NOTES:
    - The test cases will NOT be run on a machine with GPU access, nor be
      suitable for using any other machine learning techniques.

    - You can pass state forward to your agent on the next turn by assigning
      any pickleable object to the self.context attribute.
    **********************************************************************
    """
    def score(self, state):
        # euristic= number of my moves-no of opponent player moves
        own_loc = state.locs[state.player()]
        #print("own loc ",own_loc)
        own_liberties = state.liberties(own_loc)
        opponent_loc=state.locs[1-state.player()]
        #print("opp loc ",opponent_loc)
        opponent_liberties = state.liberties(opponent_loc)
        
        return len(own_liberties)-len(opponent_liberties)
    
    def principal_variation_search(self,state,depth):
        alpha = float("-inf")
        beta = float("inf")
        #best_score = float("-inf")
       # print("Best score ",best_score)
        v=-float('inf')
        #print("v ",v)
        actions=state.actions()
        if actions:
            best_move = actions[0]
        else:
            best_move=None
        maximizingPlayer=True
        for i, action  in enumerate(actions):
            new_state=state.result(action)
            if i==0:
                v=max(v,self._min(new_state,depth-1, alpha, beta, maximizingPlayer))
            else:
                v=max(v,self._min(new_state,depth-1, alpha,alpha+1, maximizingPlayer))
                if v>alpha:
                    v=max(v,self._min(new_state,depth-1, alpha, beta, maximizingPlayer))
            if v>alpha:
                alpha=v
                best_move=action
            return best_move
                
            

    def _max(self,state,depth, alpha, beta, maximizingPlayer):
        
        if state.terminal_test():
            return state.utility(state.player())
    
    # New conditional depth limit cutoff
        if depth <= 0:  # "==" could be used, but "<=" is safer 
            return self.score(state)

        v = float("inf")
        for a in state.actions():
            # the depth should be decremented by 1 on each call
            v = max(v, self._min(state.result(a), depth - 1, alpha,beta,maximizingPlayer))
        return v

        
    def _min(self, state,depth, alpha, beta, maximizingPlayer):
        
        if state.terminal_test():
            return state.utility(state.player())
    
    # New conditional depth limit cutoff
        if depth <= 0:  # "==" could be used, but "<=" is safer 
            return self.score(state)

        v = float("inf")
        for a in state.actions():
            # the depth should be decremented by 1 on each call
            v = min(v, self._max(state.result(a), depth - 1, alpha,beta,maximizingPlayer))
        return v    

    
    def get_action(self, state):
        """ Employ an adversarial search technique to choose an action
        available in the current state calls self.queue.put(ACTION) at least

        This method must call self.queue.put(ACTION) at least once, and may
        call it as many times as you want; the caller will be responsible
        for cutting off the function after the search time limit has expired.

        See RandomPlayer and GreedyPlayer in sample_players for more examples.

        **********************************************************************
        NOTE: 
        - The caller is responsible for cutting off search, so calling
          get_action() from your own code will create an infinite loop!
          Refer to (and use!) the Isolation.play() function to run games.
        **********************************************************************
        """
        # TODO: Replace the example implementation below with your own search
        #       method by combining techniques from lecture
        #
        # EXAMPLE: choose a random move without any search--this function MUST
        #          call self.queue.put(ACTION) at least once before time expires
        #          (the timer is automatically managed for you)
        depth=1
        while True:
            self.queue.put(self.principal_variation_search(state,depth))
            #self.context=self.queue
            depth+=1
            #print("Queue ", self.queue)
          
