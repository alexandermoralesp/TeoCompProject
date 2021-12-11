import random
import time
import csv

from automata import Automata
from solve import solve

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
   

def k_states_compare_performance(k, iterations):
    # Tupla de tuplas (algo, execution_time, length))
    algo_time_len = ( 
                  [Automata.AEE_algo, 0, 0],
                  [Automata.HDM_algo, 0, 0],
                  [Automata.NCE_algo, 0, 0], 
                  [Automata.NCD_algo, 0, 0]
                )
    for i in range(iterations):
        # Generate random automata of k states
        start_state, end_state_list, transition_list = generate_random_automata(k)
        for j in range(len(algo_time_len)):
            # Get algo
            algo = algo_time_len[j][0]
            # Execute algo
            start_time = time.time()
            regex = solve(k, start_state, end_state_list, transition_list, algo)
            end_time = time.time()
            # Add execution time
            algo_time_len[j][1] += (end_time-start_time)
            algo_time_len[j][2] += (len(regex) if regex is not None else 0)

    # Return
    return algo_time_len
            
def test_compare_performance(min, max):
    metrics_list = []
    print()
    print("--------------")
    print("EXECUTING:")
    print("--------------")
    for i in range(min, max+1):
        k = i
        print("Procesando con k={}".format(k))
        algo_time_len = k_states_compare_performance(k, 1000)
        metrics_list.append( (k, algo_time_len) )

    # PRINT & SAVE RESULTS
    print()
    print("--------------")
    print("RESULTS:")
    print("--------------")

    algos = [algo for algo, _, _ in  metrics_list[1][1]]
    header = ["k",]
    header.extend(algos)

    # Dispaly time
    with open('time_result.csv', 'w', newline="") as f:     
        writer = csv.writer(f)
        writer.writerow(header)
        print("TIME")
        for k, metr in metrics_list:
            data = [k,]
            print(k, end="\t")
            for _, time, _ in metr:
                data.append(time)
                print(time, end="\t")
            writer.writerow(data)
            print()


    # Dispaly length
    with open('length_result.csv', 'w', newline="") as f:  
        writer = csv.writer(f)
        writer.writerow(header)
        print("LENGTH")
        for k, metr in metrics_list:
            data = [k,]
            print(k, end="\t")
            for _, _, lenght in metr:
                data.append(lenght)
                print(lenght, end="\t")
            writer.writerow(data)
            print()



if __name__ == "__main__":
    test_compare_performance(0,32)