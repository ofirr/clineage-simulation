function [new_mutation_table] = convert_to_mutation_table_with_header(run, mutation_table, has_root)

%{
e.g.
names	Run1_C_14	Run1_C_16	Run1_C_17	Run1_C_18	Run1_C_20	Run1_C_22	Run1_C_24	Run1_C_25	Run1_C_26	Run1_C_27	Run1_C_28	Run1_C_29	Run1_C_31	Run1_C_33	Run1_C_34	Run1_C_36	Run1_C_38	Run1_C_39	Run1_C_40	Run1_C_41	Run1_C_42	Run1_C_43	Root
LOC_1	NaN	24	24	NaN	25	23	23	NaN	NaN	NaN	NaN	23	24	24	24	NaN	NaN	NaN	NaN	NaN	24	26	19
LOC_2	NaN	31	27	NaN	25	NaN	24	NaN	NaN	NaN	NaN	25	NaN	25	29	NaN	28	NaN	NaN	26	27	NaN	20
LOC_3	12	13	13	NaN	11	NaN	11	NaN	NaN	NaN	12	12	12	11	12	12	NaN	12	NaN	11	12	12	7
LOC_4	NaN	11	11	NaN	11	11	11	NaN	NaN	11	NaN	NaN	NaN	11	11	11	NaN	11	NaN	11	11	NaN	7
LOC_5	11	11	13	NaN	11	11	11	NaN	NaN	NaN	11	NaN	11	11	11	NaN	NaN	11	NaN	11	12	NaN	7
LOC_6	23	NaN	NaN	NaN	NaN	NaN	NaN	NaN	NaN	NaN	NaN	NaN	26	NaN	NaN	NaN	NaN	NaN	NaN	NaN	NaN	NaN	16
LOC_7	NaN	NaN	17	NaN	19	NaN	NaN	NaN	NaN	NaN	17	17	19	18	18	20	NaN	17	NaN	18	NaN	NaN	13
LOC_8	25	22	24	NaN	NaN	26	NaN	NaN	NaN	25	22	23	23	NaN	NaN	23	25	NaN	NaN	25	NaN	NaN	22
LOC_9	18	NaN	NaN	NaN	NaN	NaN	NaN	NaN	NaN	NaN	18	16	19	19	19	NaN	NaN	21	NaN	19	17	NaN	15
LOC_10	NaN	NaN	NaN	NaN	NaN	NaN	NaN	NaN	NaN	NaN	NaN	NaN	NaN	NaN	NaN	NaN	NaN	NaN	NaN	NaN	NaN	NaN	17
%}

% get the indexes of the leaves by extracting the last row of the LiveNodes
%leaves_idx = run.LiveNodes{end};
live_nodes_sizes = size(run.LiveNodes);
live_nodes_final_row = run.LiveNodes(live_nodes_sizes(1),:);
all_leaves_idx = horzcat(live_nodes_final_row{:});

% get number of microsatellite loci
num_of_ms_loci = size(mutation_table, 1);

% create row header for mutation table
row_header = 'LOC_' + string(1:num_of_ms_loci);
row_header = cellstr(row_header);

% create column header for mutation table
% column_header = { run.Nodes{1}(leaves_idx).Name };
column_header = string();
global_leaves_idx=0;
for cell_type = 1:length(live_nodes_final_row)
    leaves_idx_array = live_nodes_final_row(cell_type);
    leaves_idx = leaves_idx_array{end};
    for col = 1:length(leaves_idx)
        global_leaves_idx = global_leaves_idx + 1;
        leaf_id = leaves_idx(col);
        column_header(global_leaves_idx) = run.Nodes{cell_type,1}(leaf_id).Name;
    end
end
column_header = cellstr(column_header);
disp(column_header);
disp(row_header);
if has_root == true
    % add root cell at the end of the column
    column_header{1, size(column_header, 2) + 1} = 'root';
end

% create a mutation table with column header, row header
new_mutation_table = array2table(...
    mutation_table, ...
    'VariableNames', column_header, ...
    'RowNames', row_header ...
);

% set dimension name for mutation table
new_mutation_table.Properties.DimensionNames{1} = 'names';
