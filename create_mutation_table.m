function [mutation_table] = create_mutation_table(run, num_of_ms_loci)

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
        mutation_table(row, col) = run.Nodes{1,1}(leaf_id).InternalStates.MS(col);
       
    end
    
end

% create a row/column header for mutation table
column_header = 'LOC_' + string(1:num_of_ms_loci);
column_header = cellstr(column_header);
row_header = { run.Nodes{1}(leaves_idx).Name };

% create a mutation table with column header, row header
mutation_table = array2table(...
    mutation_table, ...
    'VariableNames', column_header, ...
    'RowNames', row_header ...
);

% set dimension name for mutation table
% this will allow to do `mutation_table_full.Cells`
% this will set (0,0) to `Cells` when outputted to a file
mutation_table.Properties.DimensionNames{1} = 'Cells';
