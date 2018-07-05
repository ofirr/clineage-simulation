function [mutation_table] = create_mutation_table(run, num_of_ms_loci, biallelic, allele)

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

        internal_state = run.Nodes{1,1}(leaf_id).InternalStates;

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

        mutation_table(row, col) = ms_repeat_length;

    end

end
