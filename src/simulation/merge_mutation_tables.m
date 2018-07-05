function [full_table] = merge_mutation_tables(mutation_tables)

num_alleles = length(mutation_tables);

full_table = cell( size(mutation_tables{1}) );

for row = 1:size(full_table, 1)
    
    for col = 1:size(full_table, 2)
        
        alleles = NaN(1, num_alleles);
        
        % get one allele from paternal, the other from maternal
        % combine them into a single array [p, m]
        % ii=1: paternal
        % ii=2: maternal
        for ii = 1:length(mutation_tables)

            mutation_table = mutation_tables(ii);
            mutation_table = mutation_table{1, 1};
            
            alleles(ii) = mutation_table(row, col);

        end
        
        full_table(row, col) = { alleles };
        
    end
    
end
