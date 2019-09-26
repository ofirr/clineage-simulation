function [mutation_table] = create_mutation_table(run, num_of_ms_loci, biallelic, allele)

% get the indexes of the leaves by extracting the last row of the LiveNodes
%leaves_idx = run.LiveNodes{end};

live_nodes_sizes = size(run.LiveNodes);
live_nodes_final_row = run.LiveNodes(live_nodes_sizes(1),:);
all_leaves_idx = horzcat(live_nodes_final_row{:});

% create a mutation table
% row: ms_id
% column: cell ID
% cell: ms repeat length
mutation_table = NaN( num_of_ms_loci, length(all_leaves_idx) );

global_leaves_idx = 0;

for cell_type = 1:length(live_nodes_final_row)
    leaves_idx_array = live_nodes_final_row(cell_type);
    leaves_idx = leaves_idx_array{end};

    for col = 1:length(leaves_idx)

        global_leaves_idx = global_leaves_idx + 1;

        for row = 1:num_of_ms_loci

            leaf_id = leaves_idx(col);
            
            % disp([cell_type, col, row, leaf_id]);
            
            internal_state = run.Nodes{cell_type,1}(leaf_id).InternalStates;

            if biallelic
                % biallelic
                switch allele
                    case 1
                        % paternal
                        ms_repeat_length = internal_state.MS1(row);
                    case 2
                        % maternal
                        ms_repeat_length = internal_state.MS2(row);
                    otherwise
                        error('allele must be either 1 (Paternal) or 2 (Maternal)');
                end
            else
                % monoallelic
                ms_repeat_length = internal_state.MS(row);
            end

            mutation_table(row, global_leaves_idx) = ms_repeat_length;

        end

    end

end
