function [new_mutation_table] = convert_to_mutation_table_with_header(run, mutation_table)

% get the indexes of the leaves by extracting the last row of the LiveNodes
leaves_idx = run.LiveNodes{end};

% get number of microsatellite loci
num_of_ms_loci = size(mutation_table, 2);

% create a row/column header for mutation table
column_header = 'LOC_' + string(1:num_of_ms_loci);
column_header = cellstr(column_header);
row_header = { run.Nodes{1}(leaves_idx).Name };

% create a mutation table with column header, row header
new_mutation_table = array2table(...
    mutation_table, ...
    'VariableNames', column_header, ...
    'RowNames', row_header ...
);

% set dimension name for mutation table
% this will allow to do `mutation_table_full.Cells`
% this will set (0,0) to `Cells` when outputted to a file
new_mutation_table.Properties.DimensionNames{1} = 'Cells';
