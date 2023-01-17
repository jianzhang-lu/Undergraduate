import networkx as nx
import matplotlib.pyplot as plt
from random import uniform


def Fruchterman_Reingold_Layout(data: dict):
    """
    @brief:
        Use Fruchterman-Reingold algorithm to set the location of each nodes in the canvas.
        Based on the theory of particle physics, FR algorithm simulates the nodes in the figure as atoms and calculates the position relationship between the nodes by simulating the force field between the atoms.
    @args:
        data: The data informing the distances between CDR3 sequences in the form of a dictionary.
              For example, {'1': {'2':1,'3':1,'4':1,'5':1},'2':{'1':1,'3':2,'4':2,'5':2},'3':{'1':1,'2':2,'4':3,'5':3,'7':1},'4':{'1':1,'2':2,'3':3,'5':4,'10':20},'5':{'1':1,'2':2,'3':3,'4':4},'6':{'7':1},'7':{'3':1,'6':1,'8':5},'8':{'9':2,'10':1,'7':5},'9':{'8':2},'10':{'8':1,'11':1,'4':20},'11':{'10':1,'12':1},'12':{'11':1}}
    @returns:
        position_transfer_node_name: A dictionary that contains the position information of each nodes in 'data'.
                                    For example, {'1': (-1.3415900978472386, 3.950743264276085), '2': (1.4153516858854327, 4.607296162785044), '3'...}
    """  
    
    # Calculate the total number of nodes in the data
    nodes_num = len(data.keys())
    # Randomize the initial position of each nodes
    pos_init = [(uniform(-1, 1), uniform(-1, 1)) for _ in range(nodes_num)]
    # A dictionary used to store position(tuple) data.
    position = {}
    # A dictionary used to refer to nodes' name from nodes' index
    node_name = {}
    # A dictionary used to refer to nodes' index from nodes' name
    node_ID = {}   
    
    # In convenience for further computing, create index for each node
    for index, nodeID in enumerate(data): 
        position[index] = pos_init[index] 
        node_name[index] = nodeID
        node_ID[nodeID] = index
    # if we print 'position', we can get {'1': (0.9648264980223817, 0.9387763208098376), '2': (0.2266536410934179, -0.9114787342707582), '3': (-0.9918897116831851, -0.7320549459017323), '4'

    def Coulombian_Force(node1_index: int, node2_index: int, position: dict, nodes_num: int):
        """
        @brief: Calculate the coulombian force between the nodes.
        @args:
            node1_index: the index of a node1
            node2_index: the index of a node2
            position: A dictionary used to store position(tuple) data
            nodes_num: the number of total nodes in the project(it is related to the k parameter which represents the Coulomb force coefficient)
        
        @returns:
            (force_x,force_y): a tuple informing the coulombian force (strength and direction) on node in position1. 
            
        """  
        # The parameters of coulombian force
        k = 1/300
        q = 1
        
        # Calculate the distance between two nodes
        position1 = position[node1_index]
        position2 = position[node2_index]
        dx = position1[0] - position2[0]
        dy = position1[1] - position2[1]
        distance = pow((pow(dx, 2) + pow(dy, 2)), 0.5)
        
        # Calculate the force
        # 0,0001 is used to avoid the 'zero divided error' caused by float computing.
        force = k*q*q/(distance**2 + 0.0001)
                
        # Break down the force into x and y directions
        r = pow(dx, 2)/(pow(dy, 2) + 0.00001)
        force_x = force*r/(r + 1)
        force_y = force*1/(r + 1)
        
        if dx < 0:
            force_x = -force_x
        if dy < 0:
            force_y = -force_y
        return force_x, force_y
    
    def tensile_force(node1_index: int, node2_index: int, position: dict, edge_weight: float, nodes_num: int):
        """
        @brief: Calculate the tensile force between the nodes.
        @args:
            node1_index: the index of a node1
            node2_index: the index of a node2
            position: A dictionary used to store position(tuple) data
            edge_weight: the weight of the edge between node1 and node2
            nodes_num: the number of total nodes in the project(it is related to the k parameter which represents the Coulomb force coefficient)
        
        @returns:
            (force_x,force_y): a tuple informing the tensile force (strength and direction) on node in position1. 
            
        """ 
        # The parameters of coulombian force
        k2 = (1/300) * edge_weight/8
        position1 = position[node1_index]
        position2 = position[node2_index]
        dx = position1[0] - position2[0]
        dy = position1[1] - position2[1]
        distance = pow((pow(dx, 2) + pow(dy, 2)), 0.5)
        
        # Calculate the force
        force = k2*distance
        
        # Break down the force into x and y directions
        r = pow(dx, 2)/(pow(dy, 2) + 0.000000001)
        force_x = force*r/(r + 1)
        force_y = force*1/(r + 1)
        
        if dx > 0:
            force_x = -force_x
        if dy > 0:
            force_y = -force_y
        return force_x, force_y
    
    def summary_force_situation(node_index, data_dic, node_name_dic, node_ID_dic, position_dic, nodes_num):
        """
        @brief: Calculating the overall force condition of one node
        @args:
            node_index: the index of a node in the position dictionary
            data_dic: The data informing the distances between CDR3 sequences in the form of a dictionary.
            node_name_dic: A dictionary used to refer to nodes' name from nodes' index
            node_ID_dic: A dictionary used to refer to nodes' index from nodes' name
            position_dic: A dictionary used to store position(tuple) data.
            nodes_num: The number of total nodes in the project(it is related to the k parameter which represents the Coulomb force coefficient)
        
        @returns:
            (force_x,force_y): a tuple informing the total force (strength and direction) on node in position1. 
            
        """ 
        # The initial force is 0
        force_x_summary = 0
        force_y_summary = 0
        
        # Calculate the Coulombian Force
        for i in range(0, nodes_num):
            if i != node_index:
                # Calculate the force
                force_x_summary = force_x_summary + Coulombian_Force(node_index, i, position_dic, nodes_num)[0]
                force_y_summary = force_y_summary + Coulombian_Force(node_index, i, position_dic, nodes_num)[1]
        
        # Calculate the Tensile Force
        for linked_node in data_dic[node_name_dic[node_index]]:
            
            # Find the position of the linked nodes and their edge weight
            i = node_ID_dic[linked_node]
            edge_weight = data_dic[node_name_dic[node_index]][linked_node]
            
            # Calculate the force
            force_x_summary = force_x_summary + tensile_force(node_index, i, position_dic, edge_weight, nodes_num)[0]
            force_y_summary = force_y_summary + tensile_force(node_index, i, position_dic, edge_weight, nodes_num)[1]
        
        return force_x_summary, force_y_summary
    
    def change_position(data_diction, node_name_diction, node_ID_diction, position_diction, nodes_num):
        """
        @brief: Calculating the changes in the position of every nodes
        @args:
            data_dictiom: The data informing the distances between CDR3 sequences in the form of a dictionary.
            node_name_diction: A dictionary used to refer to nodes' name from nodes' index
            node_ID_diction: A dictionary used to refer to nodes' index from nodes' name
            position_diction: A dictionary used to store position(tuple) data.
            nodes_num: The number of total nodes in the project(it is related to the k parameter which represents the Coulomb force coefficient)
        
        @returns:
            position_new: the new position dictionary of every nodes.
            
        """ 
        # Set the time for every movement
        dt = 0.3
        # Define the frictional force
        f = 0.000001
        # Define the mass of each node
        m = 1
        # 'position_new' is a dictionary storing the new positions
        position_new = {}
        
        # Calculate the force situation of each nodes
        for self_index in position_diction:
            position_now = position_diction[self_index]
            force_x = summary_force_situation(self_index, data_diction, node_name_diction, node_ID_diction, position_diction, nodes_num)[0]
            force_y = summary_force_situation(self_index, data_diction, node_name_diction, node_ID_diction, position_diction, nodes_num)[1]
            
            # if the sum of force is greater than the friction, the node can still move to its next position.
            if pow(force_x, 2) + pow(force_y, 2) > pow(f, 2):
            
                # f*t = m*v according to the theorem of impulse.
                v_x = (force_x - f)*dt/m
                v_y = (force_y - f)*dt/m
                
                # dx = v*dt
                dx = v_x*dt
                dy = v_y*dt
                position_new[self_index] = (position_now[0]+dx, position_now[1]+dy)
            
            else:
                # If the sum of force is equal to or smaller than the friction, the node can't move.
                position_new[self_index] = (position_now[0], position_now[1])
        
        return position_new
    
    # Iterate for 700 times:
    for iteration in range(700):
        position = change_position(data, node_name, node_ID, position, nodes_num)

    # Change the node_index into node_name, but reserve the position data of each nodes
    position_transfer_node_name = {}
    for node_index in position:
        position_transfer_node_name[node_name[node_index]] = position[node_index]

    return position_transfer_node_name


def Create_Graph(data: dict):
    """
    @brief:
        Create an undirected network graph using the data in 'filename'.
    @args:
        data: The data informing the distances between CDR3 sequences in the form of a dictionary.
                  For example, {'1':{'2':1,'3':1,'4':1,'5':1},'2':{'1':1,'3':2,'4':2,'5':2},'3':{'1':1,'2':2,'4':3,'5':3,'7':1},'4':{'1':1,'2':2,'3':3,'5':4,'10':20},'5':{'1':1,'2':2,'3':3,'4':4},'6':{'7':1},'7':{'3':1,'6':1,'8':5},'8':{'9':2,'10':1,'7':5},'9':{'8':2},'10':{'8':1,'11':1,'4':20},'11':{'10':1,'12':1},'12':{'11':1}}
    @returns:
        graph: The undirected graph with nodes (different CDR3 sequences) and edges (the alignment score or distance between the CDR3 sequences)
    """

    # initialize an undirected graph
    graph = nx.Graph()  
    
    # Then input the distance data into the undirected graph
    for start_node in data:
        for end_node in data[start_node]:
            
            # 'weight' is the distance between CDR3 sequences.
            graph.add_edge(str(start_node), str(end_node), weight=data[start_node][end_node])

    return graph


def Show_Community(data: dict, G, community, output):
    """
    @brief:
        visualize the clustering of the CDR3 sequence data
    @args:
        G: The undirected graph with nodes and edges
        community: A list informing the clusters.
        For example, [['1','2','3'],['5'],['4'],['6','7','8','9','10','11','12']].
        output: The path and title of output plots
    @returns:
        Showing the plot
    """

    # 'clusters' is used to store which cluster each node belongs to. After finishing storing: {node1:"cluster1", node2:"cluster3"......}
    clusters = {}
    # 'labels' is used to store the name of each node in the graph.After finishing storing: {node1："node1"，......}
    labels = {}
    # 'index' represents the index of each cluster

    for index in range(0, len(community)):
        # 'someone_cluster' represents each cluster
        someone_cluster = community[index]

        for node in someone_cluster:
            # Store the new node name.
            labels[node] = node
            # Store the node-cluster correspondence.
            clusters[node] = index

    # Parameters for visualizing the nodes 
    colors = ['r', 'g', 'b', 'c', 'y', 'm', 'lime', 'slateblue', 'violet', 'lightcoral', 'khaki', 'aqua']
    shapes = ['v', 'D', 'o', '^', '<', '*', 's']
    
    # position: Using Fruchterman-Reingold algrithm to set the location of each node in the canvas.
    # 'position' parameter will be used in drawing the plot.
    position = Fruchterman_Reingold_Layout(data)

    # To use the default function in networkx to do the position-calculating.
    # position = nx.spring_layout(G)
    
    # 1. Visualize the nodes.
    for index in range(0, len(community)):
        someone_cluster = community[index]
        for _ in someone_cluster:
            # use the draw_networkx_nodes function in the networkx
            nx.draw_networkx_nodes(G, position, nodelist=someone_cluster,
                                   node_color=colors[index % 12],
                                   node_shape=shapes[index % 7],
                                   node_size=60,
                                   alpha=1)

    # 2. Visualize the edges
    # 2.1 Grouping data
    # Separate the inter-cluster edges and the intra-cluster edges.
    edges = {'between_cluster': []}
    # networkx.Graph.edges function，
    # Returns all nodes that are connected to each node in G.
    # For example, [('1', '5'), ('5', '4'), ('2', '5'), ('3', '5'), ('4', '5')]

    for link in G.edges():
        # inter-cluster edges     
        if clusters[link[0]] != clusters[link[1]]:  
            edges['between_cluster'].append(link)
        else:
            # intra-cluster edges      
            if clusters[link[0]] not in edges:
                edges[clusters[link[0]]] = [link]
            else:
                edges[clusters[link[0]]].append(link)
    
    # 2.2 visualizing data
    for cluster_index in edges: 
        someone_edgelist = edges[cluster_index]
        
        # inter-cluster edges
        if cluster_index == 'between_cluster': 
            nx.draw_networkx_edges(G, position,
                                   edgelist=someone_edgelist,
                                   width=0.1, alpha=0.4, edge_color='black')
        # intra-cluster edges
        else:
            nx.draw_networkx_edges(G, position,
                                   edgelist=someone_edgelist,
                                   width=0.3, alpha=0.4, edge_color=colors[cluster_index])

    # 3. Visualizing the labels
    nx.draw_networkx_labels(G, position, labels, font_size=7)
    
    # 4. Showing the plot
    plt.axis('off')
    figure = plt.gcf()
    figure.set_size_inches(28, 16)
    plt.savefig(output+".png", bbox_inches='tight', dpi=300)


def Visualization_Main(distance: dict, community: list, output: str):
    """
    @brief:
        the summative function of the visualization process
    @args:
        filename: The .txt file that produced by distance calculating process. The data should be in the form of a dictionary.
                  For example, {'1':{'2':1,'3':1,'4':1,'5':1},'2':{'1':1,'3':2,'4':2,'5':2},'3':{'1':1,'2':2,'4':3,'5':3,'7':1},'4':{'1':1,'2':2,'3':3,'5':4,'10':20},'5':{'1':1,'2':2,'3':3,'4':4},'6':{'7':1},'7':{'3':1,'6':1,'8':5},'8':{'9':2,'10':1,'7':5},'9':{'8':2},'10':{'8':1,'11':1,'4':20},'11':{'10':1,'12':1},'12':{'11':1}}
        
        community: The .txt file in the form of a list informing the clusters. 
                  For example, [['1','2','3'],['5'],['4'],['6','7','8','9','10','11','12']].
        output: The path and title of output plots
    @returns:
        Showing the plot
    """

    print("--------------------------------------")
    print("Start Visualization")
    print("--------------------------------------")

    # Change the node name in raw distance data from integer to string format
    new_distance = {}
    for i in distance:
        new_distance[str(i)] = {}
        for j in distance[i]:
            new_distance[str(i)][str(j)] = distance[i][j]
    
    # Change the node name in raw clustering data from integer to string format
    new_community = []
    for i in community:
        temp_community = []
        for j in i:
            temp_community.append(str(j))
        new_community.append(temp_community)

    # To scale the edge_weight to (0,10]. The reason is that:
    # 1. There may be non-positive edge_weight which can cause error;
    # 2. the (0,10] range will better visualize the cluster result, according to our trials.
    edge_list = []
    for start_node in distance:
        for end_node in distance[start_node]:
            edge_list.append(distance[start_node][end_node])

    edge_min = min(edge_list)
    edge_max = max(edge_list)
    for start_node in distance:
        for end_node in distance[start_node]:
            distance[start_node][end_node] = (distance[start_node][end_node] - edge_min) * 10 / (edge_max - edge_min)

    # visualization
    d_graph = Create_Graph(new_distance)
    Show_Community(new_distance, d_graph, new_community, output)
    print("End Visualization")
    return
