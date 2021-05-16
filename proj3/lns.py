
def lns(warehouse, rand_solutionlist):
    iterations = 200
    
    solutionlist = rand_solutionlist
    best_solutionlist = solutionlist

#    while not stop_criterion:
#   TODO: stop_criterion
    for i in range(iterations):
        candidate_solution = repair(destroy(solutionlist))
        if accept(solutionlist, candidate_solution):
            solutionlist = candidate_solution

        storage_sl, cost_sl = warehouse.run(solutionlist)
        storage_best, cost_best = warehouse.run(best_solutionlist)
        if cost_sl < cost_best:
            best_solutionlist = solutionlist

    return best_solutionlist
        
        
        
def destroy(sl): # TODO
    return sl
    
def repair(sl): # TODO
    return sl
    
def accept(sl, sl_cand): # TODO
    return True # or False
