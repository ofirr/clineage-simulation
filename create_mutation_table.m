function [mutation_table] = create_mutation_table(run, num_of_ms_loci, ms_repeat_lengths)

% get the indexes of the leaves by extracting the last row of the LiveNodes
leaves_idx = run.LiveNodes{end};

% create a mutation table
% row: cell ID
% column: ms ID
% cell: ms repeat length
mutation_table = NaN( length(leaves_idx), num_of_ms_loci );

for col = 1:num_of_ms_loci
        
    for row = 1:length(leaves_idx)
        
        leaf_id = leaves_idx(row);
        
        % use idx to get the actual ms repeat length
        ms_repeat_length_idx = run.Nodes{1,1}(leaf_id).InternalStates.MS(col);
        mutation_table(row, col) = ms_repeat_lengths(ms_repeat_length_idx);
       
    end
    
end
