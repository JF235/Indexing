from heapq import heapify, heappop, heappush
from bisect import insort
from np.linalg import norm

class HNSW:
    def __init__(self, num_layers: int):
        self.num_layers = num_layers
        self.layers = [[] for _ in range(num_layers)]
    
    def __len__(self):
        return len(self.layers[0])
    
    def search(self, query, ef = 1):
        if len(self) == 0:
            return []

        best_v = 0
        for layer in reversed(self.layers):
            best_d, best_v = self.search_layer(layer, query, entry_point, ef=1)[0]
            if layer[best_v][2]:
                best_v = layer[best_v][2]
            else:
                return self.search_layer(layer, query, best_v, ef=ef)
            
    
    def search_layer(self, layer, query, entry_point, ef = 1):
        # Layer is a list of tuples (Graph) 
        # Node: (vector, list of edges, index of the level below)
        vec = lambda idx: layer[idx][0]
        edges = lambda idx: layer[idx][1]
        
        best = (norm(vec(idx) - query), entry_point)
        
        nns = [best]
        visit = set(best)
        cadidates = [best]
        heapify(cadidates)
        
        while candidates:
            curr_vert = heappop(candidates)
            
            # If the current vertex is further than the worst result...
            if nns[-1][0] < curr_vert[0]:
                break
            
            for e in edges(curr_vert[1]):
                d = norm(vec(e) - query)
                
                # Check if its already visited
                if (d, e) not in visit:
                    # ... if not, adds
                    visit.add((d, e))
                    
                    # and push the best candidates to the heap    
                    if d < nns[-1][0] or len(nns) < ef:
                        heappush(candidates, (d, e))
                        insort(nns, (d, e))
                        if len(nns) > ef:
                            nns.pop()
        
        return nns
    
    def insert(self, vec, efc = 10):
        
        # If the graph is empty, insert the vector in the first layer
        # and all
        if len(self) == 0:
            i = None
            for layer in reversed(self.layers):
                layer.append((vec, [], i))
                i = 0
            return

        l = self.get_insert_layer(self.num_layers, 0)

        
        
    def get_insert_layer(self, L, mL):
        l = -int(np.log(np.random.random()) * mL)
        return min(l, L)