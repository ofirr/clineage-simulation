function [mutation_table] = create_mutation_table(run, num_of_ms_loci, ms_repeat_lengths)

% get the indexes of the leaves by extracting the last row of the LiveNodes
leaves_idx = run.LiveNodes{end};

% create a mutation table
% row: ms_id
% column: cell ID
% cell: ms repeat length
mutation_table = NaN( num_of_ms_loci, length(leaves_idx) );

for col = 1:length(leaves_idx)
        
    for row = 1:num_of_ms_loci
        
        leaf_id = leaves_idx(col);
        
        % use idx to get the actual ms repeat length
        ms_repeat_length_idx = run.Nodes{1,1}(leaf_id).InternalStates.MS(row);
        mutation_table(row, col) = ms_repeat_lengths(ms_repeat_length_idx);
       
    end
    
end
