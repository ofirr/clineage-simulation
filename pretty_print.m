function pretty_print(run, mutation_table)

% get mutation table with column/row header
mutation_table_with_header = convert_to_mutation_table_with_header(run, mutation_table);

% print to screen
disp(mutation_table_with_header);
