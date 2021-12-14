import random

from automata import Automata

def generate_random_automata(n):
    # GENERATE TUPLE (start_state, end_state_list, transition_list)

    # Starting state
    start_state = random.randint(0,n)
    # End states
    n_end_states = random.randint(0,n)
    end_state_list= random.sample(range(0,n), n_end_states)
    # Transition list
    transition_list = []
    for i in range(n):
        transition_list.append( (i,0, random.randint(0,n)) )
        transition_list.append( (i,1, random.randint(0,n)) )        

    # RETURN TUPLE
    return (start_state, end_state_list, transition_list)
   

def validate_function(k, iterations):
    error_n = 0
    succes_n = 0
    for i in range(iterations):
        # Generate random automata of k states
        start_state, end_state_list, transition_list = generate_random_automata(k)
        
        # Execute and comapre
        at = Automata(k, start_state, end_state_list, transition_list)
        active_states = [i for i in range(k)]
        bf_res = at.brute_force_count_cycles(active_states)
        algo_res = at.count_cycles_fix(active_states)

        if (bf_res != algo_res):
            print ("ERROR")
            print("BF:", bf_res)
            print("ALGO FIX:", algo_res)
            at.display()
            error_n += 1
        else:
            succes_n += 1
    # Return
    print("SUCCESS: {} - ERRORS: {}".format(succes_n, error_n))


if __name__ == "__main__":
    validate_function(10,10000)