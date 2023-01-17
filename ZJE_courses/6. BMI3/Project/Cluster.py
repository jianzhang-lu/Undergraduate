import random


class Cluster:
    """
    The principles of the algorithm are from (Blondel et al., 2008)
    The formula of delta_Q (old_community --> i --> new_community) used in our codes is derived on our own.
    Ideas of function structures are partially from https://github.com/xmweijh/CommunityDetection/blob/main/Louvain.py

    This class Cluster combines all relevant attributes used in clustering and can call function self.Cluster_Main() to cluster.
    The overall principle refers to the Louvain algorithm.
    The index "modularity" can show the entire quality of the segmentation by communities in a graph.
    By constantly moving nodes to the neighbor's community, the modularity can be updated to achieve better quality.

    :attribute _G: Input dict with all network information provided
    :attribute m: The sum of all the weights in the network. (Notice: self_loop needs to times 1/2)
    :attribute final_community: A dict that records which every initial node corresponds to which cluster. It has the same length as _G. A dict instead of a list cannot be influenced by subsequent randomization.
    :attribute community: Compared to final_community, it records which current node (maybe super-nodes) corresponds to which cluster. It changes.
                          {node1: community, node2: community ...}
    :attribute community_data: A triple nested dict that records all the network information with current communities. It changes and the format is shown below.
                               {{community1: {node1: {neighbor1: weight1-1, neighbor2: weight1-2}, {node2: {neighbor3: weight2-3}} ...} }

    """

    def __init__(self, G, output_file):
        """
        @breif:
            Initialize the attributes that need to be computed in the later steps.
        @args:
            G: A dict with network information provided including the memberships and the edge weights.
            Here is an example.
            {0: {1: 1, 2: 2}, 1: {0: 1}, 2: {0: 2}}
            out_put_file: The title name of the output file.
        """
        self._G = G
        self.m = 0
        self.final_community = {}
        self.community = {}
        self.community_data = {}
        self.output = output_file

    def Set_Attributes(self):
        """
            @brief:
                Make initial calculations for the attributes to be used later.
        """

        for i in self._G.keys():
            # At first, each node serves as one community.
            self.final_community[i] = i
            # Initialize the data of each community with node and neighbor data.
            self.community_data[i] = {i: self._G[i]}
            # self.m recodes the sum of the weights
            self.m += sum([self._G[i][neighbor] for neighbor in self._G[i].keys()])
        # At first, the current community equals the final_community
        self.community = self.final_community
        # The former formula counts each weight twice (one edge connects two nodes). Here it times 1/2 adapts to the definition used in modularity.
        self.m /= 2
        return

    def Change_to_New_Community(self, candidate, self_community: dict, change_community: int, neighbor_data: dict):
        """
        @brief:
            It will be called when the node needs to be changed into one of its neighbor's communities.
            Make adjustments of the self.community and self.community_data.
        @args:
            candidate: The name of the candidate node that needs to be changed
            self_community: The
            change_community:
            neighbor_data:
        @returns:
            Nothing
            All relevant information has changed within the function.
        """
        self.community[candidate] = change_community
        # Delete the data relevant to the candidate in the original community.
        del self.community_data[self_community][candidate]
        # Updata the new data in the new community
        self.community_data[change_community].update({candidate: neighbor_data})
        return

    def First_Step(self) -> bool:
        """
        @brief:
            This is the first step to optimizing modularity. This step only allows local changes to the memberships of nodes and communities.
            Every node in the network will try to merge into the community of its neighbor. This will bring about a change in the modularity of the whole network marked as delta_Q.
            For each node, select the change with the biggest positive delta_Q and move the node into the other community. If no positive delta_Q, the node will not change.
            Iterate the first step mentioned above constantly until there is no change in any node in a round.
            Then comes the second step.
        @returns:
            Whether the second step needs to be done next. In other words, whether we can stop the whole process.
            If in the calling of the first step, there is no change for each node, it means attaining the final convergence. So, return the signal to stop the whole process.
        """

        # candidates stores all potential nodes that need to be iterated.
        candidates = list(self.community_data.keys())
        # Randomization
        random.shuffle(candidates)
        # Overall_Stop is used to judge whether the whole clustering can stop. If there is no any change for each node in the first step, it means the overall process can stop and the second step will not be called,
        Overall_Stop = True
        while True:
            # This is a judgment of whether the while loop will continue or not. If this round, the judgment keeps True, the first step can stop.
            first_step_stop = True

            # Iterate each candidate (node)
            for candidate in candidates:
                self_community = self.community[candidate]
                neighbor_data = self.community_data[self_community][candidate]
                neighbors = neighbor_data.keys()
                # Ki is a value that sum up all the weights of edges from the candidate node.
                Ki = sum(neighbor_data.values())
                # visited_communities stores all previously calculated communities in case of unnecessary repetitive calculations.
                visited_communities = set()
                # In every change, only delta_modularity needs to be calculated. But only positive delta_modularities are considered, so set the threshold as 0.
                max_delta_modularity = 0
                max_modularity_community = None
                # total_old is the sum of all linking weights in the community to which the candidate originally belonged.
                total_old = 0
                for index, edge_data in self.community_data[self_community].items():
                    # Through the formula derivation, total_old exclude the candidate itself.
                    if index != candidate:
                        total_old += sum(edge_data.values())
                # Ki_oldin is the sum of edge weights that connect the candidate node and the original old community and the self-loop cannot be summed.
                # According to the definition, the weights need to be times 2 here.
                Ki_oldin = 2 * sum([edge_value for i, edge_value in neighbor_data.items() if self.community[i] == self_community and i != candidate])

                # Iterate the neighbors of the candidate
                for neighbor in neighbors:
                    neighbor_community = self.community[neighbor]
                    # if the neighbor_community has been calculated before or the neighbor and the candidate are in the same community, the later steps can be skipped.
                    if neighbor_community in visited_communities or self_community == neighbor_community:
                        continue
                    # Ki_newin is the sum of edge weights that connect the candidate node and the neighbor's community and the weights need to be times 2
                    Ki_newin = 2 * sum([edge_value for i, edge_value in neighbor_data.items() if self.community[i] == neighbor_community])
                    # total_new is the sum of all linking weights in the community to which the neighbor's community.
                    total_new = 0

                    for index, edge_data in self.community_data[neighbor_community].items():
                        total_new += sum(edge_data.values())
                    # According to the formula derivation,delta_modularity is calculated with multiple parameters calculated before
                    delta_modularity = Ki_newin-Ki_oldin+(total_old-total_new)*Ki/self.m

                    # Only positive delta_modularity is remained. The max_delta_modularity and the corresponding community keep updated
                    if delta_modularity > max_delta_modularity:
                        max_delta_modularity = delta_modularity
                        max_modularity_community = neighbor_community
                    visited_communities.add(neighbor_community)

                # if max_modularity_community exists, then comes the change, the node needs to be moved into the others' neighbor with maximal delta_modularity
                if max_modularity_community:
                    change_community = max_modularity_community
                    self.Change_to_New_Community(candidate, self_community, change_community, neighbor_data)

                    # There is a change, the step cannot stop
                    Overall_Stop = False
                    first_step_stop = False

            # If there is no exchange in one round, the first_step_stop (True) can lead to breaking the while-loop.
            if first_step_stop:
                break
        return Overall_Stop

    def Second_Step(self):
        """
        @brief:
            This is the second step to aggregate the current communities into the super-nodes for a new network.
            After the first step, many nodes have been changed into the same communities, and the whole network attained the current stability.
            In this step, the nodes in the same community will be aggregated into a new super-node (community).
            The weights of the edges within the original community (edges between the nodes in the same community) are added to contribute to a self-loop of the new super-node.
            And the super-nodes are connected if there is one edge between the nodes which connects their original communities.
            The weights between these super-nodes are the sum of the weights from all edges between their consistent communities.
            A new network is built for another run of the first step.
        @return:
            Nothing
            All relevant information has changed within the second step.
        """
        # updated_community stores the pre-calculated communities to reduce unnecessary repetitive calculations.
        updated_community = set()
        delcommunities = set()

        # Record which community is empty and delete them.
        for i in list(self.community_data.keys()):
            if self.community_data[i] == {}:
                del self.community_data[i]
                delcommunities.add(i)
        # Search and store which nodes that originally belong to the deleted community for subsequent changes.
        ToBeChanged_communities = {i: [] for i in delcommunities}
        for node, community in self.final_community.items():
            if community in delcommunities:
                # ToBeChanged_communities is like a form: {community:[original node1,original node2], ...}
                ToBeChanged_communities[community].append(node)
        # Iterate each remained community that is not empty

        for i, community_value in self.community_data.items():
            # Sum_inner is used to calculate the weights of the self-loop
            Sum_inner = 0
            # outerNeighbors can store the new neighbor data of the newly-formed super-nodes
            outerNeighbors = {}

            for member, neighbors in community_value.items():
                # If the member (originally was a community that has many nodes) has been deleted before, the final community data should be changed for updates.
                if member in delcommunities:
                    for k in ToBeChanged_communities[member]:
                        self.final_community[k] = i
                delcommunities.discard(member)

                for neighbor, weight in neighbors.items():
                    if self.community[neighbor] == self.community[member]:
                        # If self-loop, the weight will be counted only once, so weight value times 2
                        if neighbor == member:
                            Sum_inner += weight*2
                        else:
                            # If not self-loop, the weight will be counted twice, so there is no need to do multiplication.
                            Sum_inner += weight
                    else:
                        Neighbor_community = self.community[neighbor]
                        # If the neighbor_community has been calculated completely (with the linking weights between them), the value can be directly extracted.
                        if Neighbor_community in updated_community:
                            # Check whether the key ( Neighbor_community) has been created before.
                            if Neighbor_community not in outerNeighbors.keys():
                                # outerNeighbors is also a triple nested dict.
                                outerNeighbors[Neighbor_community] = self.community_data[Neighbor_community][Neighbor_community][self.community[member]]
                            continue
                        # The link weights between different neighbors need to be constantly accumulated.
                        if Neighbor_community not in outerNeighbors.keys():
                            outerNeighbors[Neighbor_community] = weight
                        else:
                            outerNeighbors[Neighbor_community] += weight

            # Form a self-loop
            outerNeighbors[i] = Sum_inner
            self.community_data[i] = {i: outerNeighbors}
            # Update the calculated community
            updated_community.add(i)

        # The community needs to be changed. Initialize self.community and self.m
        self.community = {}
        self.m = 0
        # The new network has a different self.m, so it needs to be updated
        for i in self.community_data.keys():
            self.community[i] = i
            self.m += sum([self.community_data[i][i][neighbor] for neighbor in self.community_data[i][i].keys()])
        self.m /= 2
        return

    def Get_Communities(self):
        """
        @brief:
            Relabel the final identified communities and classify all the nodes in sorted order.
        @returns:
            A nested list with each list showing all nodes that are clustered together.
        """
        remain_community_number = []
        for i, value in self.community_data.items():
            if value != {}:
                # relabel the final communities
                remain_community_number.append(i)

        # total stores all the clusters containing nodes.
        total = [[] for _ in range(len(remain_community_number))]
        for node, BTWcommunity in self.final_community.items():
            index = remain_community_number.index(BTWcommunity)
            total[index].append(node)
        for k in total:
            k.sort()
        return total

    def Cluster_Main(self):
        """
        @brief:
            Execute the whole process and output the results.
        @returns:
            the nested list with the clustering results.
        """

        print("--------------------------------------")
        print("Start Clustering")
        print("--------------------------------------")

        # Initialize all the attributes.
        self.Set_Attributes()
        while True:
            # signal_to_stop is a signal to show whether the second step needs to be continued.
            signal_to_stop = self.First_Step()
            if signal_to_stop:
                break
            else:
                self.Second_Step()
        final_results = self.Get_Communities()
        Filename = self.output + '.txt'

        with open(Filename, 'w') as f:
            for i in range(len(final_results)):
                f.write("Community "+str(i)+": ")
                contents = str(final_results[i]).lstrip('[').rstrip("]")
                f.write(contents+"\n")
        print("End Clustering")
        return final_results
