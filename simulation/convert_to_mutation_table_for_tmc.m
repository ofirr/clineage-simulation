function [new_mutation_table] = convert_to_mutation_table_for_tmc(run, mutation_table, has_root)

%{
e.g.
names	1	2	3	4	5	6	7	8	9	10	11	12	13	14	15	16	17	18	19	20	21	22	Root
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
leaves_idx = run.LiveNodes{end};

% get number of microsatellite loci
num_of_ms_loci = size(mutation_table, 1);

% get number of cells (without root cell)
num_of_cells = length( { run.Nodes{1}(leaves_idx).Name } );

% num of rows in the table = header + num of ms loci
num_of_rows = num_of_ms_loci + 1;

% num of columns in the table = header + num of cells
num_of_cols = num_of_cells + 1;
if has_root == true
    num_of_cols = num_of_cols + 1;
end

% initialize
new_mutation_table = cell( num_of_rows, num_of_cols );

% create row header for mutation table
ms_loci_names = 'LOC_' + string(1:num_of_ms_loci);
ms_loci_names = cellstr(ms_loci_names)';

% create column header for mutation table
cell_names = { run.Nodes{1}(leaves_idx).Name };
cell_numeric_ids = num2cell( 1:size(cell_names, 2) );

if has_root == true
    % add root cell at the end of the column
    cell_names{1, size(cell_names, 2) + 1} = 'root';
    cell_numeric_ids{1, size(cell_numeric_ids, 2) + 1} = 'root';
end

% TMC_CLI expects this string
new_mutation_table(1, 1) = {'names'};

% insert cell names in the first row
% insert ms loci names in the first column
new_mutation_table(1, 2:end) = cell_names;
new_mutation_table(2:end, 1) = ms_loci_names;
new_mutation_table(2:end, 2:end) = num2cell(mutation_table);
