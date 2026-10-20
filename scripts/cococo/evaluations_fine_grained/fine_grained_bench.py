import mqt.qecc.cococo.layouts as layouts
import mqt.qecc.cococo.utils_routing as utils
import mqt.qecc.cococo.circuit_construction as circuit_construction
import mqt.qecc.cococo.internal_testing as internal_testing


#from datetime import datetime

layout_type = "triple"
m = 4
n = 4
factories = []
remove_edges = False
g, data_qubit_locs, factory_ring = layouts.gen_layout_scalable(layout_type, m, n, factories, remove_edges)
layout = {i: j for i,j in enumerate(data_qubit_locs)}
t=2


layout_rev = {j:i for i,j in enumerate(data_qubit_locs)}
def qubit(pos, schedule = None):
    if schedule is not None:
        ly_rev = {j: i for i,j in schedule["layout"].items()}
        return ly_rev[pos]
    return layout_rev[pos]



q = len(data_qubit_locs)
print("number of data qubits: ", q)
j = 8
num_gates = 4 * q
max_overlap = 8

seed = 1
dag, pairs = circuit_construction.create_random_sequential_circuit_dag(j, q, num_gates, seed) # at least num_gates gates
#print("pairs: ", pairs)
print("number of gates: ", len(pairs))


terminal_pairs = layouts.translate_layout_circuit(pairs, layout)
#print("terminal pairs: ", terminal_pairs)

router = utils.BasicRouter(g, data_qubit_locs, factories, valid_path = "cc", t=t, metric = "exact", use_dag = True)
# each layer has disjoint logical support, however it doesn't guarantee that all those gates can be physically routed at the same time on the lattice
layers = router.split_layer_terminal_pairs(terminal_pairs)
vdp_layers, _ = router.find_total_vdp_layers_dyn(layers, data_qubit_locs, router.factory_times, layout, testing = True)



# print the initial circuit with qubit number 
for i, layer in enumerate(layers):
    #print(i, layer, "\n")
    layer_trans =[]
    for gate in layer:
        layer_trans.append((qubit(gate[0]), qubit(gate[1])))
    #print("Layer", i, layer_trans , "\n")



print("Len of schedule (standard): ", len(vdp_layers))

router2 = utils.TeleportationRouter(g, data_qubit_locs, factories, valid_path="cc", t=t, metric="exact", use_dag = True, seed =  49218  )
router2.find_total_fine_grained_vdp_dyn(layers, data_qubit_locs, None, max_overlap = max_overlap, layout = layout, testing = True)
print("Len of schedule (fine grained): ", len(router2.routes_by_layer))


